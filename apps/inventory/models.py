"""
apps/inventory/models.py
========================
Production-ready models cho hệ thống kiểm kê kho vật liệu xây dựng.

Design decisions:
  - InventoryAudit  : Phiên kiểm kê (1 phiên gồm nhiều sản phẩm)
  - InventoryAuditItem : Dòng chi tiết mỗi sản phẩm trong phiên kiểm kê
  - InventoryLoss   : Phiếu hao hụt (có thể tạo từ kiểm kê HOẶC thủ công)

Discrepancy strategy:
  - KHÔNG lưu trường `discrepancy` vào DB vì nó là hàm thuần túy
    của (system_quantity, actual_quantity).
  - Dùng @property thuần Python để tính → không bao giờ lệch.
  - Khi cần aggregate trên DB (báo cáo), dùng F() expression:
        F('actual_quantity') - F('system_quantity')

UUID primary keys:
  - Tất cả đều dùng UUID (giống pattern hiện có) → dễ shard,
    không lộ sequential ID qua API.
"""

import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


# ============================================================
# 1. PHIÊN KIỂM KÊ KHO  (InventoryAudit)
# ============================================================
class InventoryAudit(models.Model):
    """
    Đại diện cho 1 đợt kiểm kê kho.
    Workflow:  DRAFT → SUBMITTED → APPROVED
                                 ↘ CANCELLED
    - KHO tạo (DRAFT), nhập số thực tế, rồi SUBMIT.
    - KE_TOAN / ADMIN duyệt (APPROVED) → điều chỉnh ProductStock
      và tự động tạo InventoryLoss cho các dòng thiếu hụt.
    """

    class Status(models.TextChoices):
        DRAFT     = 'DRAFT',     _('Đang kiểm')
        SUBMITTED = 'SUBMITTED', _('Đã nộp – chờ duyệt')
        APPROVED  = 'APPROVED',  _('Đã duyệt')
        CANCELLED = 'CANCELLED', _('Hủy')

    # ── Primary key ──────────────────────────────────────────
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ── Định danh ────────────────────────────────────────────
    audit_code = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        help_text=_("Mã phiên kiểm kê, VD: KK-20260413-001"),
    )
    audit_date = models.DateField(
        db_index=True,
        help_text=_("Ngày thực hiện kiểm kê"),
    )
    note = models.TextField(blank=True, default='')

    # ── Trạng thái ───────────────────────────────────────────
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )

    # ── Người thực hiện ──────────────────────────────────────
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='inventory_audits_created',
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='inventory_audits_approved',
    )
    approved_at  = models.DateTimeField(null=True, blank=True)
    rejection_note = models.TextField(blank=True, null=True)

    # ── Timestamps ───────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table  = 'inventory_audits'
        ordering  = ['-audit_date', '-created_at']
        indexes   = [
            # Truy vấn theo khoảng ngày + trạng thái (báo cáo)
            models.Index(fields=['audit_date', 'status'], name='idx_audit_date_status'),
            # Truy vấn tất cả phiên của 1 kế toán
            models.Index(fields=['approved_by'], name='idx_audit_approved_by'),
        ]
        verbose_name        = _('Phiên kiểm kê')
        verbose_name_plural = _('Phiên kiểm kê')

    def __str__(self):
        return f'{self.audit_code} — {self.get_status_display()}'

    # ── Computed helpers ─────────────────────────────────────
    @property
    def can_submit(self):
        return self.status == self.Status.DRAFT

    @property
    def can_approve(self):
        return self.status == self.Status.SUBMITTED

    @property
    def is_editable(self):
        return self.status == self.Status.DRAFT


# ============================================================
# 2. DÒNG CHI TIẾT KIỂM KÊ  (InventoryAuditItem)
# ============================================================
class InventoryAuditItem(models.Model):
    """
    Mỗi sản phẩm được kiểm kê trong 1 phiên.

    Về discrepancy:
      - KHÔNG lưu vào DB → tránh stale data.
      - Dùng @property cho code logic.
      - Dùng F() expression khi cần ORDER BY / aggregate trong DB:
            qs.annotate(disc=F('actual_quantity') - F('system_quantity'))
    """

    # ── FK ───────────────────────────────────────────────────
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    audit = models.ForeignKey(
        InventoryAudit,
        on_delete=models.CASCADE,
        related_name='items',
        db_index=True,
    )
    product = models.ForeignKey(
        'product.Product',
        on_delete=models.PROTECT,
        related_name='audit_items',
        db_index=True,
    )

    # ── Số liệu kiểm kê ──────────────────────────────────────
    system_quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text=_("Snapshot tồn kho hệ thống TẠI THỜI ĐIỂM tạo phiên kiểm kê"),
    )
    actual_quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_("Số lượng thực tế đếm được — do KHO nhập"),
    )
    note = models.CharField(max_length=500, blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table      = 'inventory_audit_items'
        # 1 sản phẩm chỉ xuất hiện 1 lần trong 1 phiên
        unique_together = ('audit', 'product')
        ordering      = ['product__name']
        indexes       = [
            # Truy vấn tất cả lần kiểm của 1 sản phẩm (history)
            models.Index(fields=['product'], name='idx_audit_item_product'),
        ]
        # CHECK constraint: actual_quantity phải >= 0 (cũng có MinValueValidator)
        constraints = [
            models.CheckConstraint(
                condition=models.Q(actual_quantity__gte=0),
                name='chk_audit_item_actual_qty_non_negative',
            ),
            models.CheckConstraint(
                condition=models.Q(system_quantity__gte=0),
                name='chk_audit_item_system_qty_non_negative',
            ),
        ]
        verbose_name        = _('Dòng kiểm kê')
        verbose_name_plural = _('Dòng kiểm kê')

    def __str__(self):
        return (
            f'{self.audit.audit_code} | {self.product.name} | '
            f'Hệ thống: {self.system_quantity} – Thực tế: {self.actual_quantity}'
        )

    # ── Computed: discrepancy là property, KHÔNG lưu DB ──────
    @property
    def discrepancy(self):
        """
        Chênh lệch = Thực tế − Hệ thống.
        Âm  → thiếu (hao hụt).
        Dương → thừa.
        Zero  → khớp.
        """
        return self.actual_quantity - self.system_quantity

    @property
    def discrepancy_pct(self):
        """Phần trăm chênh lệch so với hệ thống. None nếu system_quantity = 0."""
        if not self.system_quantity:
            return None
        return round((self.discrepancy / self.system_quantity) * 100, 2)

    @property
    def has_loss(self):
        """True nếu thực tế < hệ thống."""
        return self.discrepancy < 0

    @property
    def has_surplus(self):
        """True nếu thực tế > hệ thống (nhập chưa ghi nhận?)."""
        return self.discrepancy > 0


# ============================================================
# 3. PHIẾU HAO HỤT  (InventoryLoss)
# ============================================================
class InventoryLoss(models.Model):
    """
    Ghi nhận hao hụt vật liệu.

    Có thể được tạo theo 2 cách:
      a) Tự động khi KE_TOAN duyệt phiên kiểm kê có chênh lệch âm
         → audit_item được set, status = PENDING (chờ phân loại chính xác)
      b) Thủ công bởi KHO khi phát hiện hao hụt ngoài kiểm kê
         → audit_item = None

    Workflow: PENDING → APPROVED (KE_TOAN)
                      → REJECTED (KE_TOAN + lý do)
    """

    class LossType(models.TextChoices):
        DAMAGE    = 'DAMAGE',    _('Hư hỏng / Vỡ vụn')
        SHRINKAGE = 'SHRINKAGE', _('Hao hụt tự nhiên (bay hơi, khô, co ngót)')
        EXPIRED   = 'EXPIRED',   _('Hết hạn sử dụng')
        THEFT     = 'THEFT',     _('Mất mát / Trộm cắp')
        OTHER     = 'OTHER',     _('Khác')

    class Status(models.TextChoices):
        PENDING  = 'PENDING',  _('Chờ duyệt')
        APPROVED = 'APPROVED', _('Đã duyệt')
        REJECTED = 'REJECTED', _('Từ chối')

    # ── Primary key ──────────────────────────────────────────
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ── Định danh ────────────────────────────────────────────
    loss_code = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        help_text=_("Mã phiếu hao hụt, VD: HH-20260413-001"),
    )

    # ── Nguồn gốc (nullable → có thể tạo thủ công) ──────────
    audit_item = models.OneToOneField(
        InventoryAuditItem,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='loss_record',
        help_text=_("Dòng kiểm kê phát sinh hao hụt (null nếu tạo thủ công)"),
    )

    # ── Sản phẩm ─────────────────────────────────────────────
    product = models.ForeignKey(
        'product.Product',
        on_delete=models.PROTECT,
        related_name='loss_records',
        db_index=True,
    )

    # ── Số liệu ──────────────────────────────────────────────
    loss_quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text=_("Số lượng hao hụt — luôn dương"),
    )
    loss_type = models.CharField(
        max_length=10,
        choices=LossType.choices,
        default=LossType.OTHER,
        db_index=True,
    )
    loss_reason = models.TextField(
        help_text=_("Mô tả chi tiết nguyên nhân hao hụt"),
    )
    loss_date = models.DateField(
        db_index=True,
        help_text=_("Ngày phát sinh hao hụt"),
    )

    # ── Giá trị (để tính tổng thiệt hại) ────────────────────
    unit_cost = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Giá vốn/đơn vị tại thời điểm hao hụt — snapshot từ Product.base_price"),
    )

    # ── Trạng thái phê duyệt ─────────────────────────────────
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    rejection_note = models.TextField(blank=True, null=True)

    # ── Người thực hiện ──────────────────────────────────────
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='loss_records_created',
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='loss_records_reviewed',
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    # ── Timestamps ───────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory_losses'
        ordering = ['-loss_date', '-created_at']
        indexes  = [
            # Báo cáo: lọc theo loại + trạng thái
            models.Index(fields=['loss_type', 'status'], name='idx_loss_type_status'),
            # Báo cáo: lọc theo ngày + sản phẩm
            models.Index(fields=['loss_date', 'product'], name='idx_loss_date_product'),
            # Tổng hợp hao hụt theo sản phẩm
            models.Index(fields=['product', 'status'], name='idx_loss_product_status'),
        ]
        constraints = [
            # loss_quantity phải > 0 (validator + DB-level constraint)
            models.CheckConstraint(
                condition=models.Q(loss_quantity__gt=0),
                name='chk_loss_quantity_positive',
            ),
            # unit_cost phải >= 0
            models.CheckConstraint(
                condition=models.Q(unit_cost__gte=0),
                name='chk_loss_unit_cost_non_negative',
            ),
        ]
        verbose_name        = _('Phiếu hao hụt')
        verbose_name_plural = _('Phiếu hao hụt')

    def __str__(self):
        return (
            f'{self.loss_code} | {self.product.name} | '
            f'{self.loss_quantity} | {self.get_loss_type_display()}'
        )

    # ── Computed ─────────────────────────────────────────────
    @property
    def total_loss_value(self):
        """Tổng giá trị thiệt hại = loss_quantity × unit_cost"""
        return self.loss_quantity * self.unit_cost

    @property
    def is_editable(self):
        return self.status == self.Status.PENDING

    @property
    def from_audit(self):
        """True nếu hao hụt này phát sinh từ kiểm kê, False nếu tạo thủ công."""
        return self.audit_item_id is not None


