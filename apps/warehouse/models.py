import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.order.models import SalesOrder
from apps.product.models import Product


class ImportReceipt(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Chờ duyệt'),
        ('APPROVED', 'Đã duyệt'),
        ('REJECTED', 'Từ chối'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receipt_code = models.CharField(max_length=30, unique=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='import_receipts_created',
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='import_receipts_reviewed',
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    note = models.TextField(blank=True, null=True, help_text='Thu kho ghi chu khi tao')
    rejection_note = models.TextField(blank=True, null=True, help_text='Ke toan ghi ly do tu choi')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'import_receipts'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.receipt_code} - {self.get_status_display()}'

    @property
    def total_items(self):
        return self.items.count()

    @property
    def can_be_edited(self):
        return self.status in ('PENDING', 'REJECTED')


class ImportReceiptItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receipt = models.ForeignKey(ImportReceipt, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='import_items')
    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text='So luong, phai > 0',
    )
    unit_price = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Gia/don vi, khong duoc am',
    )
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'import_receipt_items'

    @property
    def subtotal(self):
        return self.quantity * self.unit_price


class ProductStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Số lượng tồn không được âm',
    )
    reserved_quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Số lượng đang giữ cho đơn hàng chờ xuất"
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_stocks'

    def __str__(self):
        return f'{self.product.name}: {self.quantity} {self.product.base_unit}'

    @property
    def available_quantity(self):
        """Tồn kho khả dụng = tồn thực tế - phần đang giữ chỗ."""
        return self.quantity - self.reserved_quantity


class ExportReceipt(models.Model):
    STATUS_CHOICES = [
        ('PREPARING', 'Chờ lấy hàng'),
        ('PENDING', 'Chờ duyệt'),
        ('APPROVED', 'Đã duyệt'),
        ('REJECTED', 'Từ chối'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receipt_code = models.CharField(max_length=30, unique=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='export_receipts_created',
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='export_receipts_reviewed',
    )
    sales_order = models.ForeignKey(
        SalesOrder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='export_receipts',
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    sales_order = models.ForeignKey(
        'order.SalesOrder',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='export_receipts',
        help_text='Đơn hàng liên quan'
    )
    note = models.TextField(blank=True, null=True, help_text='Lý do xuất kho')
    rejection_note = models.TextField(blank=True, null=True, help_text='Kế toán ghi lý do từ chối')
    pickup_photo = models.ImageField(upload_to='export_receipts/pickups/', blank=True, null=True)
    picked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='export_receipts_picked',
    )
    picked_at = models.DateTimeField(null=True, blank=True)
    stock_deducted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'export_receipts'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.receipt_code} - {self.get_status_display()}'

    @property
    def total_items(self):
        return self.items.count()

    @property
    def can_be_edited(self):
        return self.status in ('PREPARING', 'PENDING', 'REJECTED')


class ExportReceiptItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receipt = models.ForeignKey(ExportReceipt, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='export_items')
    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text='So luong, phai > 0',
    )
    unit_price = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Gia/don vi, khong duoc am',
    )
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'export_receipt_items'

    @property
    def subtotal(self):
        return self.quantity * self.unit_price
