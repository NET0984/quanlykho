from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.order.models import SalesOrder, SalesOrderItem
from apps.product.models import Category, Product, ProductUnit
from apps.warehouse.models import (
    ExportReceipt,
    ExportReceiptItem,
    ImportReceipt,
    ImportReceiptItem,
    ProductStock,
)


class Command(BaseCommand):
    help = "Seed sample data for dashboard, orders, warehouse, and product screens."

    @transaction.atomic
    def handle(self, *args, **options):
        now = timezone.now()

        users = self._ensure_users()
        products = self._ensure_catalog()
        self._ensure_stocks(products)
        self._ensure_sales_orders(users["sale"], products, now)
        self._ensure_import_receipts(users, products, now)
        self._ensure_export_receipts(users, products, now)

        self.stdout.write(self.style.SUCCESS("Sample data has been seeded successfully."))
        self.stdout.write("You can log in with these demo accounts:")
        self.stdout.write("- demo_admin / Demo@123")
        self.stdout.write("- demo_sale / Demo@123")
        self.stdout.write("- demo_kho / Demo@123")
        self.stdout.write("- demo_ketoan / Demo@123")

        self.stdout.write(
            f"Summary: users={self._count_demo_users()}, products={len(products)}, "
            f"orders={self._count_demo_orders()}, imports={self._count_demo_imports()}, "
            f"exports={self._count_demo_exports()}"
        )

    def _ensure_users(self):
        User = get_user_model()
        specs = [
            {
                "username": "demo_admin",
                "full_name": "Demo Admin",
                "role": "ADMIN",
                "phone_number": "0900000001",
            },
            {
                "username": "demo_sale",
                "full_name": "Demo Sale",
                "role": "SALE",
                "phone_number": "0900000002",
            },
            {
                "username": "demo_kho",
                "full_name": "Demo Kho",
                "role": "KHO",
                "phone_number": "0900000003",
            },
            {
                "username": "demo_ketoan",
                "full_name": "Demo Ke Toan",
                "role": "KE_TOAN",
                "phone_number": "0900000004",
            },
        ]

        users = {}
        for spec in specs:
            defaults = {
                "full_name": spec["full_name"],
                "role": spec["role"],
                "phone_number": spec["phone_number"],
                "email": f"{spec['username']}@example.local",
                "is_active": True,
            }
            user, _ = User.objects.get_or_create(username=spec["username"], defaults=defaults)

            dirty = False
            for field in ["full_name", "role", "phone_number", "email"]:
                expected = defaults[field]
                if getattr(user, field) != expected:
                    setattr(user, field, expected)
                    dirty = True

            if not user.is_active:
                user.is_active = True
                dirty = True

            if not user.check_password("Demo@123"):
                user.set_password("Demo@123")
                dirty = True

            if dirty:
                user.save()

            users[spec["role"]] = user

        return {
            "admin": users["ADMIN"],
            "sale": users["SALE"],
            "kho": users["KHO"],
            "ketoan": users["KE_TOAN"],
        }

    def _ensure_catalog(self):
        categories = {}
        for name in ["Xi mang", "Sat thep", "Cat da", "Hoan thien"]:
            category, _ = Category.objects.get_or_create(name=name)
            categories[name] = category

        product_specs = [
            {
                "name": "Xi mang PCB40",
                "base_price": Decimal("92000"),
                "base_unit": "Bao",
                "category": "Xi mang",
                "units": [("Pallet", Decimal("50"))],
            },
            {
                "name": "Xi mang da dung",
                "base_price": Decimal("98000"),
                "base_unit": "Bao",
                "category": "Xi mang",
                "units": [("Pallet", Decimal("40"))],
            },
            {
                "name": "Sat thep phi 16",
                "base_price": Decimal("185000"),
                "base_unit": "Cay",
                "category": "Sat thep",
                "units": [("Bo", Decimal("10"))],
            },
            {
                "name": "Sat thep phi 10",
                "base_price": Decimal("132000"),
                "base_unit": "Cay",
                "category": "Sat thep",
                "units": [("Bo", Decimal("10"))],
            },
            {
                "name": "Cat xay to",
                "base_price": Decimal("310000"),
                "base_unit": "m3",
                "category": "Cat da",
                "units": [("Xe 5m3", Decimal("5"))],
            },
            {
                "name": "Da 1x2",
                "base_price": Decimal("420000"),
                "base_unit": "m3",
                "category": "Cat da",
                "units": [("Xe 5m3", Decimal("5"))],
            },
            {
                "name": "Gach ong 8 lo",
                "base_price": Decimal("1500"),
                "base_unit": "Vien",
                "category": "Hoan thien",
                "units": [("Pallet", Decimal("500"))],
            },
            {
                "name": "Son noi that 18L",
                "base_price": Decimal("1250000"),
                "base_unit": "Thung",
                "category": "Hoan thien",
                "units": [("Lon 5L", Decimal("0.2778"))],
            },
        ]

        products = []
        for spec in product_specs:
            defaults = {
                "base_price": spec["base_price"],
                "base_unit": spec["base_unit"],
                "category": categories[spec["category"]],
                "image_url": None,
            }
            product, _ = Product.objects.get_or_create(name=spec["name"], defaults=defaults)

            dirty = False
            if product.base_price != spec["base_price"]:
                product.base_price = spec["base_price"]
                dirty = True
            if product.base_unit != spec["base_unit"]:
                product.base_unit = spec["base_unit"]
                dirty = True
            if product.category_id != categories[spec["category"]].id:
                product.category = categories[spec["category"]]
                dirty = True
            if product.image_url is not None:
                product.image_url = None
                dirty = True
            if dirty:
                product.save()

            for unit_name, conversion_rate in spec["units"]:
                ProductUnit.objects.update_or_create(
                    product=product,
                    unit_name=unit_name,
                    defaults={"conversion_rate": conversion_rate},
                )

            products.append(product)

        return products

    def _ensure_stocks(self, products):
        qty_map = {
            "Xi mang PCB40": Decimal("850"),
            "Xi mang da dung": Decimal("620"),
            "Sat thep phi 16": Decimal("340"),
            "Sat thep phi 10": Decimal("410"),
            "Cat xay to": Decimal("120"),
            "Da 1x2": Decimal("95"),
            "Gach ong 8 lo": Decimal("18000"),
            "Son noi that 18L": Decimal("130"),
        }

        for product in products:
            ProductStock.objects.update_or_create(
                product=product,
                defaults={"quantity": qty_map.get(product.name, Decimal("0"))},
            )

    def _ensure_sales_orders(self, sale_user, products, now):
        product_map = {p.name: p for p in products}

        blueprints = [
            {
                "code": "SO-DEMO-0001",
                "customer": "Cong ty An Phat",
                "phone": "0901123456",
                "status": "DONE",
                "days_ago": 1,
                "note": "Giao trong ngay",
                "items": [
                    {"product": "Xi mang PCB40", "quantity": "120", "unit_price": "92000"},
                    {"product": "Cat xay to", "quantity": "8", "unit_price": "310000"},
                ],
            },
            {
                "code": "SO-DEMO-0002",
                "customer": "Nha thau Minh Long",
                "phone": "0901765432",
                "status": "WAITING",
                "days_ago": 2,
                "note": "Cho xuat kho dot 1",
                "items": [
                    {"product": "Sat thep phi 16", "quantity": "40", "unit_price": "185000"},
                    {"product": "Da 1x2", "quantity": "10", "unit_price": "420000"},
                ],
            },
            {
                "code": "SO-DEMO-0003",
                "customer": "Cong ty Viet Build",
                "phone": "0911222333",
                "status": "CONFIRMED",
                "days_ago": 3,
                "note": "Khach can hoa don VAT",
                "items": [
                    {"product": "Gach ong 8 lo", "quantity": "2500", "unit_price": "1500"},
                    {"product": "Xi mang da dung", "quantity": "70", "unit_price": "98000"},
                ],
            },
            {
                "code": "SO-DEMO-0004",
                "customer": "Cong ty Song Hong",
                "phone": "0911999888",
                "status": "DONE",
                "days_ago": 5,
                "note": "Don hang uu tien",
                "items": [
                    {"product": "Sat thep phi 10", "quantity": "55", "unit_price": "132000"},
                    {"product": "Cat xay to", "quantity": "12", "unit_price": "310000"},
                ],
            },
            {
                "code": "SO-DEMO-0005",
                "customer": "Nha dan Le Gia",
                "phone": "0909555444",
                "status": "CANCELLED",
                "days_ago": 8,
                "note": "Khach doi thiet ke",
                "items": [
                    {"product": "Son noi that 18L", "quantity": "8", "unit_price": "1250000"},
                ],
            },
            {
                "code": "SO-DEMO-0006",
                "customer": "Cong ty Tien Phat",
                "phone": "0905333444",
                "status": "WAITING",
                "days_ago": 11,
                "note": "Can giao tung phan",
                "items": [
                    {"product": "Xi mang PCB40", "quantity": "90", "unit_price": "92000"},
                    {"product": "Da 1x2", "quantity": "18", "unit_price": "420000"},
                ],
            },
            {
                "code": "SO-DEMO-0007",
                "customer": "Cong ty Nam Khang",
                "phone": "0912345678",
                "status": "DONE",
                "days_ago": 16,
                "note": "Da doi soat thanh toan",
                "items": [
                    {"product": "Sat thep phi 16", "quantity": "22", "unit_price": "185000"},
                    {"product": "Gach ong 8 lo", "quantity": "3000", "unit_price": "1500"},
                ],
            },
            {
                "code": "SO-DEMO-0008",
                "customer": "Nha thau Hai Dang",
                "phone": "0906777888",
                "status": "DONE",
                "days_ago": 24,
                "note": "Giao du so luong",
                "items": [
                    {"product": "Xi mang da dung", "quantity": "100", "unit_price": "98000"},
                    {"product": "Cat xay to", "quantity": "15", "unit_price": "310000"},
                ],
            },
            {
                "code": "SO-DEMO-0009",
                "customer": "Cong ty Phuoc An",
                "phone": "0908333444",
                "status": "CONFIRMED",
                "days_ago": 32,
                "note": "Hop dong moi",
                "items": [
                    {"product": "Sat thep phi 10", "quantity": "35", "unit_price": "132000"},
                    {"product": "Da 1x2", "quantity": "14", "unit_price": "420000"},
                ],
            },
            {
                "code": "SO-DEMO-0010",
                "customer": "Nha dan Hoang Gia",
                "phone": "0910666777",
                "status": "DONE",
                "days_ago": 39,
                "note": "Don nho le",
                "items": [
                    {"product": "Gach ong 8 lo", "quantity": "1600", "unit_price": "1500"},
                    {"product": "Xi mang PCB40", "quantity": "45", "unit_price": "92000"},
                ],
            },
            {
                "code": "SO-DEMO-0011",
                "customer": "Cong ty Dai Tin",
                "phone": "0909111222",
                "status": "WAITING",
                "days_ago": 43,
                "note": "Cho xe van chuyen",
                "items": [
                    {"product": "Son noi that 18L", "quantity": "6", "unit_price": "1250000"},
                ],
            },
            {
                "code": "SO-DEMO-0012",
                "customer": "Cong ty Truong An",
                "phone": "0910456123",
                "status": "DONE",
                "days_ago": 50,
                "note": "Don hoan tat",
                "items": [
                    {"product": "Xi mang da dung", "quantity": "55", "unit_price": "98000"},
                    {"product": "Sat thep phi 16", "quantity": "12", "unit_price": "185000"},
                ],
            },
        ]

        for blueprint in blueprints:
            order, _ = SalesOrder.objects.update_or_create(
                order_code=blueprint["code"],
                defaults={
                    "customer_name": blueprint["customer"],
                    "customer_phone": blueprint["phone"],
                    "created_by": sale_user,
                    "status": blueprint["status"],
                    "note": blueprint["note"],
                },
            )

            SalesOrderItem.objects.filter(order=order).delete()
            for item_spec in blueprint["items"]:
                SalesOrderItem.objects.create(
                    order=order,
                    product=product_map[item_spec["product"]],
                    quantity=Decimal(item_spec["quantity"]),
                    unit_price=Decimal(item_spec["unit_price"]),
                )

            created_at = now - timedelta(days=blueprint["days_ago"])
            SalesOrder.objects.filter(pk=order.pk).update(created_at=created_at)

    def _ensure_import_receipts(self, users, products, now):
        product_map = {p.name: p for p in products}
        blueprints = [
            {
                "code": "IR-DEMO-0001",
                "status": "APPROVED",
                "days_ago": 21,
                "note": "Nhap hang bo sung dau thang",
                "rejection_note": "",
                "items": [
                    {"product": "Xi mang PCB40", "quantity": "450", "unit_price": "88000"},
                    {"product": "Cat xay to", "quantity": "60", "unit_price": "295000"},
                ],
            },
            {
                "code": "IR-DEMO-0002",
                "status": "APPROVED",
                "days_ago": 9,
                "note": "Nhap sat theo hop dong",
                "rejection_note": "",
                "items": [
                    {"product": "Sat thep phi 16", "quantity": "120", "unit_price": "179000"},
                    {"product": "Sat thep phi 10", "quantity": "150", "unit_price": "126000"},
                ],
            },
            {
                "code": "IR-DEMO-0003",
                "status": "PENDING",
                "days_ago": 2,
                "note": "Cho ke toan duyet",
                "rejection_note": "",
                "items": [
                    {"product": "Gach ong 8 lo", "quantity": "12000", "unit_price": "1400"},
                ],
            },
            {
                "code": "IR-DEMO-0004",
                "status": "REJECTED",
                "days_ago": 5,
                "note": "Nhap son dot 2",
                "rejection_note": "Can cap nhat lai so luong thuc nhap",
                "items": [
                    {"product": "Son noi that 18L", "quantity": "45", "unit_price": "1210000"},
                ],
            },
        ]

        for blueprint in blueprints:
            reviewed_by = users["ketoan"] if blueprint["status"] in {"APPROVED", "REJECTED"} else None
            reviewed_at = (
                now - timedelta(days=max(blueprint["days_ago"] - 1, 0))
                if reviewed_by
                else None
            )

            receipt, _ = ImportReceipt.objects.update_or_create(
                receipt_code=blueprint["code"],
                defaults={
                    "created_by": users["kho"],
                    "reviewed_by": reviewed_by,
                    "status": blueprint["status"],
                    "note": blueprint["note"],
                    "rejection_note": blueprint["rejection_note"] or None,
                    "reviewed_at": reviewed_at,
                },
            )

            ImportReceiptItem.objects.filter(receipt=receipt).delete()
            for item_spec in blueprint["items"]:
                ImportReceiptItem.objects.create(
                    receipt=receipt,
                    product=product_map[item_spec["product"]],
                    quantity=Decimal(item_spec["quantity"]),
                    unit_price=Decimal(item_spec["unit_price"]),
                )

            created_at = now - timedelta(days=blueprint["days_ago"])
            ImportReceipt.objects.filter(pk=receipt.pk).update(created_at=created_at)

    def _ensure_export_receipts(self, users, products, now):
        product_map = {p.name: p for p in products}
        blueprints = [
            {
                "code": "ER-DEMO-0001",
                "status": "APPROVED",
                "days_ago": 14,
                "note": "Xuat theo don SO-DEMO-0007",
                "rejection_note": "",
                "items": [
                    {"product": "Sat thep phi 16", "quantity": "22", "unit_price": "185000"},
                    {"product": "Gach ong 8 lo", "quantity": "3000", "unit_price": "1500"},
                ],
            },
            {
                "code": "ER-DEMO-0002",
                "status": "APPROVED",
                "days_ago": 6,
                "note": "Xuat theo don SO-DEMO-0004",
                "rejection_note": "",
                "items": [
                    {"product": "Sat thep phi 10", "quantity": "55", "unit_price": "132000"},
                    {"product": "Cat xay to", "quantity": "12", "unit_price": "310000"},
                ],
            },
            {
                "code": "ER-DEMO-0003",
                "status": "PENDING",
                "days_ago": 1,
                "note": "Cho duyet xuat kho",
                "rejection_note": "",
                "items": [
                    {"product": "Xi mang PCB40", "quantity": "90", "unit_price": "92000"},
                ],
            },
            {
                "code": "ER-DEMO-0004",
                "status": "REJECTED",
                "days_ago": 4,
                "note": "Xuat kho cap toc",
                "rejection_note": "Khong du ton kho tai thoi diem duyet",
                "items": [
                    {"product": "Son noi that 18L", "quantity": "8", "unit_price": "1250000"},
                ],
            },
        ]

        for blueprint in blueprints:
            reviewed_by = users["ketoan"] if blueprint["status"] in {"APPROVED", "REJECTED"} else None
            reviewed_at = (
                now - timedelta(days=max(blueprint["days_ago"] - 1, 0))
                if reviewed_by
                else None
            )

            receipt, _ = ExportReceipt.objects.update_or_create(
                receipt_code=blueprint["code"],
                defaults={
                    "created_by": users["kho"],
                    "reviewed_by": reviewed_by,
                    "status": blueprint["status"],
                    "note": blueprint["note"],
                    "rejection_note": blueprint["rejection_note"] or None,
                    "reviewed_at": reviewed_at,
                },
            )

            ExportReceiptItem.objects.filter(receipt=receipt).delete()
            for item_spec in blueprint["items"]:
                ExportReceiptItem.objects.create(
                    receipt=receipt,
                    product=product_map[item_spec["product"]],
                    quantity=Decimal(item_spec["quantity"]),
                    unit_price=Decimal(item_spec["unit_price"]),
                )

            created_at = now - timedelta(days=blueprint["days_ago"])
            ExportReceipt.objects.filter(pk=receipt.pk).update(created_at=created_at)

    def _count_demo_users(self):
        User = get_user_model()
        return User.objects.filter(username__startswith="demo_").count()

    def _count_demo_orders(self):
        return SalesOrder.objects.filter(order_code__startswith="SO-DEMO-").count()

    def _count_demo_imports(self):
        return ImportReceipt.objects.filter(receipt_code__startswith="IR-DEMO-").count()

    def _count_demo_exports(self):
        return ExportReceipt.objects.filter(receipt_code__startswith="ER-DEMO-").count()
