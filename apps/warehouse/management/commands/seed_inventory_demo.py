from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.authentication.models import User
from apps.order.models import SalesOrder, SalesOrderItem
from apps.product.models import Category, Product
from apps.warehouse.models import ExportReceipt, ImportReceipt, ProductStock
from apps.warehouse.repositories import ExportReceiptRepository, ImportReceiptRepository


class Command(BaseCommand):
    help = 'Seed du lieu demo kho va don hang can bang cho giao dien.'

    @transaction.atomic
    def handle(self, *args, **options):
        users = self._ensure_users()
        self._clear_demo_data(users)
        products = self._get_seed_products()
        if not products:
            self.stdout.write(self.style.WARNING('Khong co san pham nao de seed du lieu demo.'))
            return
        orders = self._create_sales_orders(products, users)
        approved_export_totals = self._build_approved_export_totals(orders)
        self._create_import_receipts(products, users, approved_export_totals)
        self._create_export_receipts(orders, users)
        self.stdout.write(self.style.SUCCESS('Da seed du lieu demo: 20 don hang, 15 phieu nhap, 15 phieu xuat.'))

    def _clear_demo_data(self, users):
        ExportReceipt.objects.all().delete()
        ImportReceipt.objects.all().delete()
        SalesOrder.objects.all().delete()
        ProductStock.objects.all().delete()

    def _ensure_users(self):
        users = {}
        configs = [
            ('admin_demo', 'ADMIN', 'Admin Demo'),
            ('sale_demo', 'SALE', 'Nhân viên Sale Demo'),
            ('kho_demo', 'KHO', 'Thủ kho Demo'),
            ('ketoan_demo', 'KE_TOAN', 'Kế toán Demo'),
        ]
        for username, role, full_name in configs:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    'role': role,
                    'full_name': full_name,
                    'email': f'{username}@example.com',
                },
            )
            fields_to_update = []
            if user.role != role:
                user.role = role
                fields_to_update.append('role')
            if user.full_name != full_name:
                user.full_name = full_name
                fields_to_update.append('full_name')
            expected_email = f'{username}@example.com'
            if user.email != expected_email:
                user.email = expected_email
                fields_to_update.append('email')
            if fields_to_update:
                user.save(update_fields=fields_to_update)
            users[role] = user
        return users

    def _demo_product_specs(self):
        return [
            ('Xi măng Portland', 'Bao', '50000'),
            ('Cát vàng', 'Khối', '320000'),
            ('Đá 1x2', 'Khối', '410000'),
            ('Thép cây D16', 'Cây', '185000'),
            ('Gạch nung', 'Cục', '3200'),
            ('Sơn nội thất', 'Thùng', '540000'),
        ]

    def _demo_product_names(self):
        return [name for name, _, _ in self._demo_product_specs()]

    def _get_seed_products(self):
        existing_products = list(Product.objects.order_by('name'))
        if existing_products:
            return existing_products

        category, _ = Category.objects.get_or_create(name='Vật liệu xây dựng')
        products = []
        for name, unit, price in self._demo_product_specs():
            product, _ = Product.objects.get_or_create(
                name=name,
                defaults={
                    'base_unit': unit,
                    'base_price': Decimal(price),
                    'category': category,
                },
            )
            products.append(product)
        return products

    def _target_stock_quantity(self, index):
        return Decimal(20 + (index % 11))

    def _build_approved_export_totals(self, orders):
        totals = {}
        for order in orders:
            if order.status != 'DONE':
                continue
            for item in order.items.all():
                totals[item.product_id] = totals.get(item.product_id, Decimal('0')) + item.quantity
        return totals

    def _create_import_receipts(self, products, users, approved_export_totals):
        statuses = ['APPROVED'] * 6 + ['PENDING'] * 5 + ['REJECTED'] * 4
        creator_cycle = [users['KHO']] * 10 + [users['ADMIN']] * 5
        reviewer_cycle = [users['KE_TOAN']] * 7 + [users['ADMIN']] * 3
        reviewer_index = 0
        approved_payloads = []
        for index, product in enumerate(products):
            approved_payloads.append(
                {
                    'product_id': str(product.id),
                    'quantity': self._target_stock_quantity(index) + approved_export_totals.get(product.id, Decimal('0')),
                    'unit_price': product.base_price,
                    'note': 'Ton kho muc tieu 20-30',
                }
            )

        approved_groups = [[] for _ in range(6)]
        for index, payload in enumerate(approved_payloads):
            approved_groups[index % 6].append(payload)

        for idx, status in enumerate(statuses, start=1):
            if status == 'APPROVED':
                items = approved_groups[idx - 1]
                if not items:
                    items = [approved_payloads[(idx - 1) % len(approved_payloads)]]
            else:
                first_product = products[(idx - 1) % len(products)]
                second_product = products[idx % len(products)]
                items = [
                    {
                        'product_id': str(first_product.id),
                        'quantity': Decimal('5') + (idx % 4),
                        'unit_price': first_product.base_price,
                        'note': 'Dong demo',
                    },
                    {
                        'product_id': str(second_product.id),
                        'quantity': Decimal('3') + (idx % 3),
                        'unit_price': second_product.base_price,
                        'note': 'Dong demo 2',
                    },
                ]

            receipt = ImportReceiptRepository.create_with_items(
                {'note': f'Phieu nhap demo {idx}'},
                items,
                creator_cycle[idx - 1],
            )
            if status == 'APPROVED':
                ImportReceiptRepository.approve(receipt, reviewer_cycle[reviewer_index])
                reviewer_index += 1
            elif status == 'REJECTED':
                ImportReceiptRepository.reject(receipt, reviewer_cycle[reviewer_index], 'Tu choi demo')
                reviewer_index += 1

    def _create_sales_orders(self, products, users):
        desired_statuses = ['CONFIRMED'] * 5 + ['WAITING'] * 7 + ['DONE'] * 6 + ['CANCELLED'] * 2
        orders = []
        for idx, status in enumerate(desired_statuses, start=1):
            order = SalesOrder.objects.create(
                order_code=f'DH-DEMO-{idx:03d}',
                customer_name=f'Khach hang {idx:02d}',
                customer_phone=f'0900000{idx:03d}',
                created_by=users['SALE'],
                status=status,
                note='Don hang demo',
            )
            product = products[(idx - 1) % len(products)]
            SalesOrderItem.objects.create(
                order=order,
                product=product,
                quantity=Decimal('1') + (idx % 3),
                unit_price=product.base_price,
            )
            orders.append(order)
        return orders

    def _create_export_receipts(self, orders, users):
        waiting_orders = [order for order in orders if order.status == 'WAITING']
        done_orders = [order for order in orders if order.status == 'DONE']
        confirmed_orders = [order for order in orders if order.status == 'CONFIRMED'][:2]
        creator_cycle = [users['KHO']] * 10 + [users['ADMIN']] * 5
        reviewer_cycle = [users['KE_TOAN']] * 5 + [users['ADMIN']] * 3
        reviewer_index = 0

        for idx, order in enumerate(waiting_orders + done_orders + confirmed_orders, start=1):
            target_status = order.status
            items = [
                {
                    'product_id': str(item.product_id),
                    'quantity': item.quantity,
                    'unit_price': item.unit_price,
                    'note': f'Don {order.order_code}',
                }
                for item in order.items.all()
            ]
            receipt = ExportReceiptRepository.create_with_items(
                {
                    'note': f'Xuat hang cho don {order.order_code}',
                    'sales_order': order,
                },
                items,
                creator_cycle[idx - 1],
            )
            if target_status == 'DONE':
                ExportReceiptRepository.approve(receipt, reviewer_cycle[reviewer_index])
                reviewer_index += 1
            elif target_status == 'CONFIRMED':
                ExportReceiptRepository.reject(receipt, reviewer_cycle[reviewer_index], 'Tu choi demo')
                reviewer_index += 1
