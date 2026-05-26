from django.db import transaction
from django.utils import timezone

from apps.order.models import SalesOrder

from .models import ExportReceipt, ExportReceiptItem, ImportReceipt, ImportReceiptItem, ProductStock
from .stock_utils import build_stock_payload


class ImportReceiptRepository:
    @staticmethod
    def get_all():
        return ImportReceipt.objects.select_related('created_by', 'reviewed_by').prefetch_related('items__product').all()

    @staticmethod
    def get_by_id(receipt_id):
        try:
            return ImportReceipt.objects.select_related('created_by', 'reviewed_by').prefetch_related('items__product').get(pk=receipt_id)
        except ImportReceipt.DoesNotExist:
            return None

    @staticmethod
    def get_by_status(status):
        return ImportReceipt.objects.select_related('created_by', 'reviewed_by').prefetch_related('items__product').filter(status=status)

    @staticmethod
    def get_by_user(user):
        return ImportReceipt.objects.select_related('created_by', 'reviewed_by').prefetch_related('items__product').filter(created_by=user)

    @staticmethod
    def generate_receipt_code():
        date_str = timezone.now().strftime('%Y%m%d')
        count = ImportReceipt.objects.filter(receipt_code__startswith=f'PN-{date_str}').count() + 1
        return f'PN-{date_str}-{count:03d}'

    @staticmethod
    @transaction.atomic
    def create_with_items(receipt_data, items_data, user):
        receipt_data['receipt_code'] = ImportReceiptRepository.generate_receipt_code()
        receipt_data['created_by'] = user
        receipt_data['status'] = 'PENDING'
        receipt = ImportReceipt.objects.create(**receipt_data)
        ImportReceiptItem.objects.bulk_create(
            [
                ImportReceiptItem(
                    receipt=receipt,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    unit_price=item.get('unit_price', 0),
                    note=item.get('note', ''),
                )
                for item in items_data
            ]
        )
        return receipt

    @staticmethod
    @transaction.atomic
    def approve(receipt, reviewed_by):
        receipt.status = 'APPROVED'
        receipt.reviewed_by = reviewed_by
        receipt.reviewed_at = timezone.now()
        receipt.rejection_note = ''
        receipt.save()

        for item in receipt.items.select_related('product').all():
            stock, _ = ProductStock.objects.get_or_create(
                product=item.product,
                defaults={'quantity': 0, 'reserved_quantity': 0},
            )
            stock.quantity += item.quantity
            stock.save()
        return receipt

    @staticmethod
    def reject(receipt, reviewed_by, rejection_note):
        receipt.status = 'REJECTED'
        receipt.reviewed_by = reviewed_by
        receipt.reviewed_at = timezone.now()
        receipt.rejection_note = rejection_note
        receipt.save()
        return receipt

    @staticmethod
    @transaction.atomic
    def resubmit(receipt, items_data, note=''):
        receipt.status = 'PENDING'
        receipt.rejection_note = ''
        receipt.note = note
        receipt.reviewed_by = None
        receipt.reviewed_at = None
        receipt.save()
        receipt.items.all().delete()
        ImportReceiptItem.objects.bulk_create(
            [
                ImportReceiptItem(
                    receipt=receipt,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    unit_price=item.get('unit_price', 0),
                    note=item.get('note', ''),
                )
                for item in items_data
            ]
        )
        return receipt


class ProductStockRepository:
    @staticmethod
    def get_stock(product_id):
        try:
            return ProductStock.objects.select_related('product').get(product_id=product_id)
        except ProductStock.DoesNotExist:
            return None

    @staticmethod
    def get_all():
        return ProductStock.objects.select_related('product__category').all()

    @staticmethod
    def get_quantity(product_id):
        stock = ProductStockRepository.get_stock(product_id)
        return stock.quantity if stock else 0

    @staticmethod
    def get_stock_payload(product_id):
        return build_stock_payload(ProductStockRepository.get_quantity(product_id))


class ExportReceiptRepository:
    @staticmethod
    def get_all():
        return ExportReceipt.objects.select_related(
            'created_by',
            'reviewed_by',
            'picked_by',
            'sales_order',
        ).prefetch_related('items__product').all()

    @staticmethod
    def get_by_id(receipt_id):
        try:
            return ExportReceipt.objects.select_related(
                'created_by',
                'reviewed_by',
                'picked_by',
                'sales_order',
            ).prefetch_related('items__product').get(pk=receipt_id)
        except ExportReceipt.DoesNotExist:
            return None

    @staticmethod
    def get_by_status(status):
        return ExportReceipt.objects.select_related(
            'created_by',
            'reviewed_by',
            'picked_by',
            'sales_order',
        ).prefetch_related('items__product').filter(status=status)

    @staticmethod
    def get_by_user(user):
        return ExportReceipt.objects.select_related(
            'created_by',
            'reviewed_by',
            'picked_by',
            'sales_order',
        ).prefetch_related('items__product').filter(created_by=user)

    @staticmethod
    def generate_receipt_code():
        date_str = timezone.now().strftime('%Y%m%d')
        count = ExportReceipt.objects.filter(receipt_code__startswith=f'EX-{date_str}').count() + 1
        return f'EX-{date_str}-{count:03d}'

    @staticmethod
    @transaction.atomic
    def create_with_items(receipt_data, items_data, user):
        sales_order = receipt_data.get('sales_order')
        if sales_order:
            has_open_receipt = ExportReceipt.objects.filter(
                sales_order=sales_order,
                status__in=['PREPARING', 'PENDING', 'APPROVED'],
            ).exists()
            if has_open_receipt:
                raise ValueError(f'Don hang {sales_order.order_code} da co phieu xuat dang xu ly hoac da duyet.')

        receipt_data['receipt_code'] = ExportReceiptRepository.generate_receipt_code()
        receipt_data['created_by'] = user
        receipt_data['status'] = receipt_data.pop('initial_status', 'PENDING')
        receipt = ExportReceipt.objects.create(**receipt_data)
        ExportReceiptItem.objects.bulk_create(
            [
                ExportReceiptItem(
                    receipt=receipt,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    unit_price=item.get('unit_price', 0),
                    note=item.get('note', ''),
                )
                for item in items_data
            ]
        )

        if sales_order and sales_order.status == 'CONFIRMED':
            sales_order.status = 'WAITING'
            sales_order.save(update_fields=['status'])
        return receipt

    @staticmethod
    def _extract_order_code_from_note(note):
        if not note:
            return None
        import re

        match = re.search(r'(DH-\d{8}-\d+)', note)
        if match:
            return match.group(1)
        match = re.search(r'(DH-\d{4}-\d+)', note)
        return match.group(1) if match else None

    @staticmethod
    def _get_linked_order(receipt):
        if receipt.sales_order_id:
            return receipt.sales_order
        order_code = ExportReceiptRepository._extract_order_code_from_note(receipt.note)
        if not order_code:
            return None
        return SalesOrder.objects.filter(order_code=order_code).first()

    @staticmethod
    def _validate_stock_before_deduct(receipt):
        insufficient_items = []
        for item in receipt.items.select_related('product').all():
            stock, _ = ProductStock.objects.get_or_create(product=item.product, defaults={'quantity': 0})
            if stock.quantity < item.quantity:
                insufficient_items.append(
                    f'{item.product.name}: ton {stock.quantity} {item.product.base_unit}, can xuat {item.quantity} {item.product.base_unit}'
                )
        if insufficient_items:
            raise ValueError('Khong the xac nhan da lay hang vi ton kho khong du: ' + '; '.join(insufficient_items))

    @staticmethod
    def deduct_stock_for_receipt(receipt):
        if receipt.stock_deducted:
            return receipt
        ExportReceiptRepository._validate_stock_before_deduct(receipt)
        for item in receipt.items.select_related('product').all():
            stock, _ = ProductStock.objects.get_or_create(
                product=item.product,
                defaults={'quantity': 0, 'reserved_quantity': 0},
            )
            stock.quantity -= item.quantity
            released = item.quantity if stock.reserved_quantity >= item.quantity else stock.reserved_quantity
            stock.reserved_quantity -= released
            if stock.quantity < 0:
                stock.quantity = 0
            if stock.reserved_quantity < 0:
                stock.reserved_quantity = 0
            stock.save()
        receipt.stock_deducted = True
        receipt.save(update_fields=['stock_deducted'])
        return receipt

    @staticmethod
    def restore_stock_for_receipt(receipt):
        if not receipt.stock_deducted:
            return receipt
        for item in receipt.items.select_related('product').all():
            stock, _ = ProductStock.objects.get_or_create(
                product=item.product,
                defaults={'quantity': 0, 'reserved_quantity': 0},
            )
            stock.quantity += item.quantity
            stock.save()
        receipt.stock_deducted = False
        receipt.save(update_fields=['stock_deducted'])
        return receipt

    @staticmethod
    @transaction.atomic
    def mark_as_picked(receipt, picked_by, pickup_photo=None):
        ExportReceiptRepository.deduct_stock_for_receipt(receipt)

        receipt.status = 'PENDING'
        receipt.picked_by = picked_by
        receipt.picked_at = timezone.now()
        if pickup_photo is not None:
            receipt.pickup_photo = pickup_photo
        receipt.rejection_note = ''
        receipt.save()

        order = ExportReceiptRepository._get_linked_order(receipt)
        if order and order.status == 'WAITING':
            order.status = 'PICKED'
            order.save(update_fields=['status'])
        if receipt.stock_deducted:
            return receipt
        return receipt

    @staticmethod
    @transaction.atomic
    def approve(receipt, reviewed_by):
        if receipt.status != 'PENDING':
            raise ValueError('Chi co the duyet phieu dang cho duyet.')

        receipt.status = 'APPROVED'
        receipt.reviewed_by = reviewed_by
        receipt.reviewed_at = timezone.now()
        receipt.rejection_note = ''
        receipt.save()

        order = ExportReceiptRepository._get_linked_order(receipt)
        if order and order.status == 'PICKED':
            order.status = 'DONE'
            order.save(update_fields=['status'])
        if receipt.stock_deducted:
            return receipt
        # Trừ tồn kho
        for item in receipt.items.select_related('product').all():
            stock, _ = ProductStock.objects.get_or_create(
                product=item.product,
                defaults={'quantity': 0, 'reserved_quantity': 0}
            )
            stock.quantity -= item.quantity
            released = item.quantity if stock.reserved_quantity >= item.quantity else stock.reserved_quantity
            stock.reserved_quantity -= released
            if stock.quantity < 0:
                stock.quantity = 0  # Không cho âm kho
            if stock.reserved_quantity < 0:
                stock.reserved_quantity = 0
            stock.save()

        # Tự động cập nhật đơn hàng → DONE
        order = receipt.sales_order
        if order is None:
            order_code = ExportReceiptRepository._extract_order_code_from_note(receipt.note)
            if order_code:
                from apps.order.models import SalesOrder
                order = SalesOrder.objects.filter(order_code=order_code).first()

        if order and order.status in ['WAITING', 'CONFIRMED']:
            order.status = 'DONE'
            order.save(update_fields=['status'])

        return receipt

    @staticmethod
    def reject(receipt, reviewed_by, rejection_note):
        receipt.status = 'REJECTED'
        receipt.reviewed_by = reviewed_by
        receipt.reviewed_at = timezone.now()
        receipt.rejection_note = rejection_note
        receipt.save()

        if receipt.stock_deducted:
            ExportReceiptRepository.restore_stock_for_receipt(receipt)
        # Nhả phần đã giữ chỗ khi phiếu bị từ chối.
        else:
            # Chưa deduct nhưng đã reserve → nhả reserved_quantity
            for item in receipt.items.select_related('product').all():
                stock, _ = ProductStock.objects.get_or_create(
                    product=item.product,
                    defaults={'quantity': 0, 'reserved_quantity': 0}
                )
                released = min(item.quantity, stock.reserved_quantity)
                stock.reserved_quantity = max(stock.reserved_quantity - released, 0)
                stock.save(update_fields=['reserved_quantity', 'last_updated'])

        # Trả order về WAITING để có thể tạo phiếu xuất mới
        order = ExportReceiptRepository._get_linked_order(receipt)
        if order and order.status in ['WAITING', 'PICKED']:
            order.status = 'WAITING'
            order.save(update_fields=['status'])
        return receipt

    @staticmethod
    @transaction.atomic
    def resubmit(receipt, items_data, note=''):
        """Thủ kho sửa lại phiếu bị từ chối và gửi lại."""

        # Bước 1: Nhả stock cũ
        if receipt.stock_deducted:
            ExportReceiptRepository.restore_stock_for_receipt(receipt)
        else:
            # Nhả reserved_quantity từ lần submit trước
            for item in receipt.items.select_related('product').all():
                stock, _ = ProductStock.objects.get_or_create(
                    product=item.product,
                    defaults={'quantity': 0, 'reserved_quantity': 0}
                )
                released = min(item.quantity, stock.reserved_quantity)
                stock.reserved_quantity = max(stock.reserved_quantity - released, 0)
                stock.save(update_fields=['reserved_quantity', 'last_updated'])

        # Bước 2: Kiểm tra tồn kho mới + reserve
        requested_by_product = {}
        for item in items_data:
            product_id = item['product_id']
            requested_by_product[product_id] = requested_by_product.get(product_id, 0) + item['quantity']

        for product_id, requested_qty in requested_by_product.items():
            stock, _ = ProductStock.objects.select_for_update().get_or_create(
                product_id=product_id,
                defaults={'quantity': 0, 'reserved_quantity': 0}
            )
            if stock.available_quantity < requested_qty:
                product_name = stock.product.name if stock.product else 'Sản phẩm'
                raise ValueError(f'Không đủ tồn khả dụng để gửi lại phiếu cho {product_name}.')

        for product_id, requested_qty in requested_by_product.items():
            stock = ProductStock.objects.select_for_update().get(product_id=product_id)
            stock.reserved_quantity += requested_qty
            stock.save(update_fields=['reserved_quantity', 'last_updated'])

        # Bước 3: Reset trạng thái phiếu
        receipt.status = 'PREPARING' if receipt.sales_order_id else 'PENDING'
        receipt.rejection_note = ''
        receipt.note = note
        receipt.reviewed_by = None
        receipt.reviewed_at = None
        receipt.picked_by = None
        receipt.picked_at = None
        receipt.pickup_photo = None
        receipt.save()

        # Bước 4: Thay items
        receipt.items.all().delete()
        ExportReceiptItem.objects.bulk_create([
            ExportReceiptItem(
                receipt=receipt,
                product_id=item['product_id'],
                quantity=item['quantity'],
                unit_price=item.get('unit_price', 0),
                note=item.get('note', ''),
            )
            for item in items_data
        ])

        # Bước 5: Cập nhật order
        order = ExportReceiptRepository._get_linked_order(receipt)
        if order and order.status in ['CONFIRMED', 'WAITING', 'PICKED']:
            order.status = 'WAITING'
            order.save(update_fields=['status'])

        return receipt
