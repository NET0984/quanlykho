from __future__ import annotations

import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.inventory.models import InventoryAudit, InventoryAuditItem, InventoryLoss
from apps.order.models import SalesOrder, SalesOrderItem
from apps.product.models import Category, Product, ProductUnit
from apps.reports.models import ReportExportLog
from apps.warehouse.models import (
    ExportReceipt,
    ExportReceiptItem,
    ImportReceipt,
    ImportReceiptItem,
    ProductStock,
)


class Command(BaseCommand):
    help = "Tao du lieu mau lien quan cho toan bo he thong."

    def add_arguments(self, parser):
        parser.add_argument("--categories", type=int, default=8)
        parser.add_argument("--products", type=int, default=40)
        parser.add_argument("--units-per-product", type=int, default=2)
        parser.add_argument("--orders", type=int, default=20)
        parser.add_argument("--import-receipts", type=int, default=12)
        parser.add_argument("--export-receipts", type=int, default=10)
        parser.add_argument("--audits", type=int, default=3)
        parser.add_argument("--losses", type=int, default=6)
        parser.add_argument("--report-logs", type=int, default=12)
        parser.add_argument("--seed", type=int, default=2026)
        parser.add_argument("--reset", action="store_true")

    def handle(self, *args, **options):
        rng = random.Random(options["seed"])

        with transaction.atomic():
            if options["reset"]:
                self._reset_data()

            users = self._ensure_users()
            categories = self._seed_categories(options["categories"])
            products = self._seed_products(options["products"], categories, rng)
            self._seed_units(products, options["units_per_product"], rng)
            self._seed_stocks(products, rng)

            orders = self._seed_orders(options["orders"], products, users, rng)
            self._seed_import_receipts(options["import_receipts"], products, users, rng)
            self._seed_export_receipts(options["export_receipts"], products, users, orders, rng)
            self._seed_inventory_audits(options["audits"], products, users, rng)
            self._seed_manual_losses(options["losses"], products, users, rng)
            self._seed_report_logs(options["report_logs"], users, rng)

        self.stdout.write(self.style.SUCCESS("Seed data complete."))

    def _reset_data(self):
        ReportExportLog.objects.all().delete()
        InventoryLoss.objects.all().delete()
        InventoryAuditItem.objects.all().delete()
        InventoryAudit.objects.all().delete()
        ExportReceiptItem.objects.all().delete()
        ExportReceipt.objects.all().delete()
        ImportReceiptItem.objects.all().delete()
        ImportReceipt.objects.all().delete()
        SalesOrderItem.objects.all().delete()
        SalesOrder.objects.all().delete()
        ProductStock.objects.all().delete()
        ProductUnit.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

    def _ensure_users(self):
        User = get_user_model()
        users = {}
        defaults = [
            ("admin_seed", "ADMIN"),
            ("kho_seed", "KHO"),
            ("ketoan_seed", "KE_TOAN"),
            ("sale_seed", "SALE"),
        ]
        for username, role in defaults:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                    "full_name": username.replace("_", " ").title(),
                    "role": role,
                    "is_active": True,
                },
            )
            if created:
                user.set_password("12345678")
                user.save(update_fields=["password"])
            users[role] = user
        return users

    def _seed_categories(self, count):
        base_names = [
            "Gach", "Thep", "Xi mang", "Cat", "Da", "Go", "Son", "Ong nuoc",
            "Vat lieu hoan thien", "Thiet bi dien", "Tam lop", "Gach op lat",
        ]
        existing = Category.objects.count()
        categories = []
        for i in range(count):
            name = base_names[i % len(base_names)]
            if i >= len(base_names):
                name = f"{name} {existing + i + 1}"
            obj, _ = Category.objects.get_or_create(name=name)
            categories.append(obj)
        return categories

    def _seed_products(self, count, categories, rng):
        existing = Product.objects.count()
        products = []
        base_units = ["bao", "kg", "tan", "m3", "cay", "hop"]
        for i in range(count):
            name = f"San pham {existing + i + 1:03d}"
            category = rng.choice(categories)
            base_price = Decimal(str(rng.randint(50, 5000)))
            base_unit = rng.choice(base_units)
            product, _ = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "base_price": base_price,
                    "base_unit": base_unit,
                    "image_url": "",
                },
            )
            products.append(product)
        return products

    def _seed_units(self, products, units_per_product, rng):
        unit_candidates = [
            ("le", Decimal("1")),
            ("bo", Decimal("5")),
            ("thung", Decimal("10")),
            ("kien", Decimal("20")),
        ]
        for product in products:
            choices = rng.sample(unit_candidates, k=min(units_per_product, len(unit_candidates)))
            for unit_name, rate in choices:
                ProductUnit.objects.get_or_create(
                    product=product,
                    unit_name=unit_name,
                    defaults={"conversion_rate": rate},
                )

    def _seed_stocks(self, products, rng):
        for product in products:
            stock, _ = ProductStock.objects.get_or_create(product=product)
            quantity = Decimal(str(rng.randint(50, 500)))
            reserved = Decimal(str(rng.randint(0, 30)))
            stock.quantity = quantity
            stock.reserved_quantity = min(reserved, quantity)
            stock.save(update_fields=["quantity", "reserved_quantity"])

    def _seed_orders(self, count, products, users, rng):
        statuses = ["CONFIRMED", "WAITING", "PICKED", "DONE"]
        orders = []
        start = SalesOrder.objects.count() + 1
        for i in range(count):
            order_code = f"SO-{timezone.now():%Y%m%d}-{start + i:04d}"
            order = SalesOrder.objects.create(
                order_code=order_code,
                customer_name=f"Khach hang {start + i:03d}",
                customer_phone=f"09{rng.randint(10000000, 99999999)}",
                created_by=users.get("SALE") or users.get("ADMIN"),
                status=rng.choice(statuses),
                note="Don hang mau",
            )
            for product in rng.sample(products, k=rng.randint(1, 4)):
                unit_price = (product.base_price or Decimal("0")) * Decimal("1.1")
                SalesOrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=Decimal(str(rng.randint(1, 20))),
                    unit_price=unit_price,
                )
            orders.append(order)
        return orders

    def _seed_import_receipts(self, count, products, users, rng):
        statuses = ["PENDING", "APPROVED", "REJECTED"]
        start = ImportReceipt.objects.count() + 1
        for i in range(count):
            status = rng.choice(statuses)
            receipt = ImportReceipt.objects.create(
                receipt_code=f"PN-{timezone.now():%Y%m%d}-{start + i:04d}",
                created_by=users.get("KHO") or users.get("ADMIN"),
                reviewed_by=users.get("KE_TOAN") if status == "APPROVED" else None,
                status=status,
                note="Phieu nhap mau",
                reviewed_at=timezone.now() if status == "APPROVED" else None,
            )
            for product in rng.sample(products, k=rng.randint(1, 4)):
                qty = Decimal(str(rng.randint(5, 50)))
                ImportReceiptItem.objects.create(
                    receipt=receipt,
                    product=product,
                    quantity=qty,
                    unit_price=(product.base_price or Decimal("0")) * Decimal("0.9"),
                    note="Nhap hang",
                )
                if status == "APPROVED":
                    stock, _ = ProductStock.objects.get_or_create(product=product)
                    stock.quantity += qty
                    stock.save(update_fields=["quantity"])

    def _seed_export_receipts(self, count, products, users, orders, rng):
        statuses = ["PREPARING", "PENDING", "APPROVED"]
        start = ExportReceipt.objects.count() + 1
        for i in range(count):
            status = rng.choice(statuses)
            receipt = ExportReceipt.objects.create(
                receipt_code=f"PX-{timezone.now():%Y%m%d}-{start + i:04d}",
                created_by=users.get("KHO") or users.get("ADMIN"),
                reviewed_by=users.get("KE_TOAN") if status == "APPROVED" else None,
                status=status,
                note="Xuat hang mau",
                reviewed_at=timezone.now() if status == "APPROVED" else None,
                sales_order=rng.choice(orders) if orders else None,
            )
            for product in rng.sample(products, k=rng.randint(1, 4)):
                qty = Decimal(str(rng.randint(1, 15)))
                ExportReceiptItem.objects.create(
                    receipt=receipt,
                    product=product,
                    quantity=qty,
                    unit_price=(product.base_price or Decimal("0")) * Decimal("1.2"),
                    note="Xuat hang",
                )
                if status == "APPROVED":
                    stock, _ = ProductStock.objects.get_or_create(product=product)
                    stock.quantity = max(Decimal("0"), stock.quantity - qty)
                    stock.save(update_fields=["quantity"])

    def _seed_inventory_audits(self, count, products, users, rng):
        statuses = [InventoryAudit.Status.DRAFT, InventoryAudit.Status.SUBMITTED, InventoryAudit.Status.APPROVED]
        start = InventoryAudit.objects.count() + 1
        for i in range(count):
            status = rng.choice(statuses)
            audit = InventoryAudit.objects.create(
                audit_code=f"KK-{timezone.now():%Y%m%d}-{start + i:03d}",
                audit_date=timezone.now().date(),
                status=status,
                note="Phien kiem ke mau",
                created_by=users.get("KHO") or users.get("ADMIN"),
                approved_by=users.get("KE_TOAN") if status == InventoryAudit.Status.APPROVED else None,
                approved_at=timezone.now() if status == InventoryAudit.Status.APPROVED else None,
            )
            for product in rng.sample(products, k=min(len(products), rng.randint(5, 12))):
                stock = getattr(product, "stock", None)
                system_qty = stock.quantity if stock else Decimal("0")
                delta = Decimal(str(rng.randint(-5, 5)))
                actual_qty = max(Decimal("0"), system_qty + delta)
                item = InventoryAuditItem.objects.create(
                    audit=audit,
                    product=product,
                    system_quantity=system_qty,
                    actual_quantity=actual_qty,
                    note="Kiem ke",
                )
                if status == InventoryAudit.Status.APPROVED and actual_qty < system_qty:
                    InventoryLoss.objects.create(
                        loss_code=f"HH-{timezone.now():%Y%m%d}-{audit.id.hex[:6]}-{product.id.hex[:4]}",
                        audit_item=item,
                        product=product,
                        loss_quantity=system_qty - actual_qty,
                        loss_type=InventoryLoss.LossType.SHRINKAGE,
                        loss_reason="Hao hut khi kiem ke",
                        loss_date=timezone.now().date(),
                        unit_cost=product.base_price or Decimal("0"),
                        status=InventoryLoss.Status.APPROVED,
                        created_by=users.get("KHO") or users.get("ADMIN"),
                        reviewed_by=users.get("KE_TOAN"),
                        reviewed_at=timezone.now(),
                    )

    def _seed_manual_losses(self, count, products, users, rng):
        start = InventoryLoss.objects.count() + 1
        for i in range(count):
            product = rng.choice(products)
            InventoryLoss.objects.create(
                loss_code=f"HH-TT-{timezone.now():%Y%m%d}-{start + i:04d}",
                audit_item=None,
                product=product,
                loss_quantity=Decimal(str(rng.randint(1, 5))),
                loss_type=InventoryLoss.LossType.DAMAGE,
                loss_reason="Hao hut thu cong",
                loss_date=timezone.now().date(),
                unit_cost=product.base_price or Decimal("0"),
                status=InventoryLoss.Status.PENDING,
                created_by=users.get("KHO") or users.get("ADMIN"),
                reviewed_by=None,
                reviewed_at=None,
            )

    def _seed_report_logs(self, count, users, rng):
        report_types = [choice[0] for choice in ReportExportLog.ReportType.choices]
        formats = [choice[0] for choice in ReportExportLog.ExportFormat.choices]
        for _ in range(count):
            ReportExportLog.objects.create(
                report_type=rng.choice(report_types),
                export_format=rng.choice(formats),
                exported_by=users.get("ADMIN") or users.get("KE_TOAN"),
                filter_params={"sample": True},
                row_count=rng.randint(5, 200),
            )
