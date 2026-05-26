# 🏗️ Production-Ready Backend Design
## Inventory Discrepancy + Loss Classification + Report Export

> Plugs directly into the existing **TeLiet_Quanlykho** project (Django + MySQL + CBV + Repo–Service pattern).

---

## 1. Database Design — Django Models

### 1.1 New Models (apps/inventory/models.py)

```python
import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from apps.product.models import Product


# ============================================================
# PHIÊN KIỂM KÊ KHO (Audit Session)
# Một đợt kiểm kê có thể gồm nhiều dòng sản phẩm
# ============================================================
class InventoryAudit(models.Model):
    """Đợt kiểm kê kho — ghi nhận số liệu thực tế theo từng phiên"""

    STATUS_CHOICES = [
        ('DRAFT',     'Đang kiểm'),
        ('SUBMITTED', 'Đã nộp'),
        ('APPROVED',  'Đã duyệt'),
        ('CANCELLED', 'Hủy'),
    ]

    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    audit_code   = models.CharField(max_length=30, unique=True, db_index=True)
    audit_date   = models.DateField(db_index=True)
    note         = models.TextField(blank=True, null=True)
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT', db_index=True)

    created_by   = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='inventory_audits_created'
    )
    approved_by  = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='inventory_audits_approved'
    )
    approved_at  = models.DateTimeField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_audits'
        ordering = ['-audit_date', '-created_at']
        indexes = [
            models.Index(fields=['audit_date', 'status']),
        ]

    def __str__(self):
        return f'{self.audit_code} — {self.get_status_display()}'


# ============================================================
# DÒNG CHI TIẾT KIỂM KÊ (Audit Line)
# ============================================================
class InventoryAuditItem(models.Model):
    """Từng dòng sản phẩm trong phiên kiểm kê"""

    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    audit            = models.ForeignKey(InventoryAudit, on_delete=models.CASCADE, related_name='items')
    product          = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='audit_items', db_index=True)

    system_quantity  = models.DecimalField(
        max_digits=15, decimal_places=2,
        help_text='Số lượng HỆ THỐNG tại thời điểm kiểm kê (snapshot từ ProductStock)'
    )
    actual_quantity  = models.DecimalField(
        max_digits=15, decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Số lượng THỰC TẾ đếm được'
    )
    note             = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'inventory_audit_items'
        unique_together = ('audit', 'product')   # 1 sản phẩm/1 phiên kiểm kê
        indexes = [
            models.Index(fields=['product']),
        ]

    @property
    def discrepancy(self):
        """Chênh lệch = Thực tế - Hệ thống. Âm = thiếu (hao hụt)."""
        return self.actual_quantity - self.system_quantity

    @property
    def has_loss(self):
        return self.discrepancy < 0


# ============================================================
# PHIẾU GHI NHẬN HAO HỤT (Loss Record)
# Được tạo tự động khi phiên kiểm kê có chênh lệch âm
# ============================================================
class InventoryLoss(models.Model):
    """Hao hụt kho — được phân loại và ghi nhận chính thức"""

    LOSS_TYPE_CHOICES = [
        ('DAMAGE',    'Hư hỏng / Vỡ vụn'),
        ('SHRINKAGE', 'Hao hụt tự nhiên (bay hơi, khô, co ngót)'),
        ('EXPIRED',   'Hết hạn sử dụng'),
        ('THEFT',     'Mất mát / Trộm cắp'),
        ('OTHER',     'Khác'),
    ]

    STATUS_CHOICES = [
        ('PENDING',  'Chờ xử lý'),
        ('APPROVED', 'Đã duyệt'),
        ('REJECTED', 'Từ chối'),
    ]

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loss_code      = models.CharField(max_length=30, unique=True, db_index=True)

    audit_item     = models.OneToOneField(
        InventoryAuditItem, on_delete=models.PROTECT,
        related_name='loss_record', null=True, blank=True,
        help_text='Liên kết đến dòng kiểm kê nếu hao hụt phát sinh từ kiểm kê'
    )
    product        = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='loss_records', db_index=True)

    loss_quantity  = models.DecimalField(
        max_digits=15, decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text='Số lượng bị hao hụt (luôn dương)'
    )
    loss_type      = models.CharField(max_length=10, choices=LOSS_TYPE_CHOICES, db_index=True)
    loss_reason    = models.TextField(help_text='Mô tả chi tiết lý do hao hụt')
    loss_date      = models.DateField(db_index=True)

    unit_cost      = models.DecimalField(
        max_digits=19, decimal_places=4, default=0,
        validators=[MinValueValidator(0)],
        help_text='Giá vốn tại thời điểm hao hụt'
    )

    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING', db_index=True)

    created_by     = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='loss_records_created'
    )
    reviewed_by    = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='loss_records_reviewed'
    )
    reviewed_at    = models.DateTimeField(null=True, blank=True)
    rejection_note = models.TextField(blank=True, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_losses'
        ordering = ['-loss_date', '-created_at']
        indexes = [
            models.Index(fields=['loss_type', 'status']),
            models.Index(fields=['loss_date', 'product']),
            models.Index(fields=['product', 'status']),
        ]

    def __str__(self):
        return f'{self.loss_code} — {self.get_loss_type_display()} — {self.loss_quantity}'

    @property
    def total_loss_value(self):
        return self.loss_quantity * self.unit_cost


# ============================================================
# NHẬT KÝ XUẤT BÁO CÁO (Export Log)
# ============================================================
class ReportExportLog(models.Model):
    """Ghi lại mọi lần xuất báo cáo cho audit trail"""

    FORMAT_CHOICES = [
        ('EXCEL', 'Excel (.xlsx)'),
        ('PDF',   'PDF'),
    ]

    REPORT_TYPE_CHOICES = [
        ('STOCK_SUMMARY',   'Báo cáo tổng hợp tồn kho'),
        ('IMPORT_HISTORY',  'Lịch sử nhập kho'),
        ('EXPORT_HISTORY',  'Lịch sử xuất kho'),
        ('LOSS_REPORT',     'Báo cáo hao hụt'),
        ('AUDIT_REPORT',    'Báo cáo kiểm kê'),
        ('DISCREPANCY',     'Báo cáo chênh lệch kho'),
    ]

    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report_type   = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, db_index=True)
    export_format = models.CharField(max_length=5, choices=FORMAT_CHOICES)
    exported_by   = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='report_exports'
    )
    exported_at   = models.DateTimeField(auto_now_add=True, db_index=True)
    filter_params = models.JSONField(default=dict, help_text='Tham số lọc đã dùng khi xuất')
    row_count     = models.IntegerField(default=0)

    class Meta:
        db_table = 'report_export_logs'
        ordering = ['-exported_at']
        indexes = [
            models.Index(fields=['report_type', 'exported_at']),
        ]
```

### 1.2 Modified Model — ExportReceipt (add FK)

```python
# Thêm vào apps/warehouse/models.py — ExportReceipt class
sales_order = models.ForeignKey(
    'order.SalesOrder',
    on_delete=models.SET_NULL,
    null=True, blank=True,
    related_name='export_receipts',
    help_text='Đơn hàng liên quan (thay thế parse regex từ note)'
)
```

### 1.3 Modified Model — ProductStock (thêm reserved)

```python
# Thêm vào apps/warehouse/models.py — ProductStock class
reserved_quantity = models.DecimalField(
    max_digits=15, decimal_places=2,
    default=0,
    validators=[MinValueValidator(0)],
    help_text='Số lượng đang được giữ cho đơn hàng chờ xuất'
)

@property
def available_quantity(self):
    """Tồn kho khả dụng = tồn - đang giữ"""
    return self.quantity - self.reserved_quantity
```

---

## 2. API Design

### Base URL: `/api/`
> Auth: `Authorization: Bearer <JWT>` hoặc Session Cookie

---

### 2.1 Inventory Audit (Kiểm kê kho)

| Method | URL | Roles | Mô tả |
|--------|-----|-------|--------|
| `GET`  | `/api/inventory/audits/` | KHO, KE_TOAN, ADMIN | Danh sách phiên kiểm kê |
| `POST` | `/api/inventory/audits/` | KHO, ADMIN | Tạo phiên + snapshot stock tự động |
| `GET`  | `/api/inventory/audits/{id}/` | KHO, KE_TOAN, ADMIN | Chi tiết + chênh lệch từng dòng |
| `PATCH`| `/api/inventory/audits/{id}/items/{item_id}/` | KHO, ADMIN | Cập nhật actual_quantity |
| `POST` | `/api/inventory/audits/{id}/submit/` | KHO, ADMIN | Nộp (DRAFT → SUBMITTED) |
| `POST` | `/api/inventory/audits/{id}/approve/` | KE_TOAN, ADMIN | Duyệt → điều chỉnh stock + tạo LossRecord |
| `POST` | `/api/inventory/audits/{id}/cancel/` | ADMIN | Hủy phiên |

**POST /audits/ — Request:**
```json
{
  "audit_date": "2026-04-13",
  "note": "Kiểm kê quý I/2026",
  "product_ids": ["uuid-1", "uuid-2"]
}
```

**GET /audits/{id}/ — Response:**
```json
{
  "id": "uuid",
  "audit_code": "KK-20260413-001",
  "audit_date": "2026-04-13",
  "status": "SUBMITTED",
  "items": [
    {
      "id": "uuid",
      "product_id": "uuid",
      "product_name": "Xi măng Hà Tiên",
      "system_quantity": 50.00,
      "actual_quantity": 45.50,
      "discrepancy": -4.50,
      "has_loss": true,
      "note": ""
    }
  ],
  "summary": {
    "total_products": 20,
    "products_with_loss": 3,
    "products_with_surplus": 1,
    "total_discrepancy_qty": -12.50
  }
}
```

---

### 2.2 Inventory Loss (Hao hụt)

| Method | URL | Roles | Mô tả |
|--------|-----|-------|--------|
| `GET`  | `/api/inventory/losses/` | KHO, KE_TOAN, ADMIN | Danh sách (filter: type, status, date, product) |
| `POST` | `/api/inventory/losses/` | KHO, ADMIN | Tạo hao hụt thủ công |
| `GET`  | `/api/inventory/losses/{id}/` | KHO, KE_TOAN, ADMIN | Chi tiết |
| `PATCH`| `/api/inventory/losses/{id}/` | KHO, ADMIN | Cập nhật loss_type / loss_reason |
| `POST` | `/api/inventory/losses/{id}/approve/` | KE_TOAN, ADMIN | Duyệt → trừ kho |
| `POST` | `/api/inventory/losses/{id}/reject/` | KE_TOAN, ADMIN | Từ chối + lý do |
| `GET`  | `/api/inventory/losses/stats/` | KE_TOAN, ADMIN | Thống kê theo type / tháng / sản phẩm |

**POST /losses/ — Request:**
```json
{
  "product_id": "uuid",
  "loss_quantity": 4.50,
  "loss_type": "DAMAGE",
  "loss_reason": "Bao xi măng bị thủng trong vận chuyển",
  "loss_date": "2026-04-13",
  "unit_cost": 95000.00
}
```

**GET /losses/stats/ — Response:**
```json
{
  "by_type": [
    { "loss_type": "DAMAGE",    "label": "Hư hỏng", "count": 5, "total_quantity": 25.0, "total_value": 2375000 },
    { "loss_type": "SHRINKAGE", "label": "Hao hụt tự nhiên", "count": 3, "total_quantity": 8.5, "total_value": 680000 }
  ],
  "by_month": [
    { "month": "2026-04", "total_quantity": 33.5, "total_value": 3055000 }
  ],
  "top_products": [
    { "product_name": "Xi măng Hà Tiên PCB40", "total_quantity": 15.0, "total_value": 1425000 }
  ]
}
```

---

### 2.3 Discrepancy Report

| Method | URL | Roles | Mô tả |
|--------|-----|-------|--------|
| `GET` | `/api/inventory/discrepancy/` | KHO, KE_TOAN, ADMIN | So sánh hệ thống vs kiểm kê gần nhất |

**Query params:** `?product_id=&category_id=`

**Response:**
```json
{
  "generated_at": "2026-04-13T10:48:00+07:00",
  "items": [
    {
      "product_id": "uuid",
      "product_name": "Xi măng Hà Tiên",
      "system_quantity": 50.00,
      "last_audit_date": "2026-04-01",
      "last_actual_qty": 45.50,
      "discrepancy": -4.50,
      "discrepancy_pct": -9.0,
      "status": "SHORTAGE"
    }
  ],
  "summary": { "shortage_count": 3, "surplus_count": 1, "ok_count": 16 }
}
```

---

### 2.4 Report Export

| Method | URL | Roles | Query params |
|--------|-----|-------|---|
| `GET` | `/api/reports/stock-summary/export/` | KE_TOAN, ADMIN | `?format=excel\|pdf&date_from=&date_to=` |
| `GET` | `/api/reports/import-history/export/` | KE_TOAN, ADMIN | `?format=excel\|pdf&date_from=&date_to=` |
| `GET` | `/api/reports/export-history/export/` | KE_TOAN, ADMIN | `?format=excel\|pdf&date_from=&date_to=` |
| `GET` | `/api/reports/loss-report/export/` | KE_TOAN, ADMIN | `?format=excel\|pdf&loss_type=&date_from=&date_to=` |
| `GET` | `/api/reports/discrepancy/export/` | KE_TOAN, ADMIN | `?format=excel\|pdf` |
| `GET` | `/api/reports/audit-report/export/` | KE_TOAN, ADMIN | `?format=excel\|pdf&audit_id=` |

**Response (Excel):**
```
HTTP 200
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename="ton-kho-20260413.xlsx"
<binary>
```

---

## 3. Architecture

### 3.1 Folder Structure

```
apps/inventory/
├── __init__.py
├── apps.py
├── models.py               ← InventoryAudit, InventoryLoss, ReportExportLog
├── serializers.py          ← DRF serializers + validation
├── permissions.py          ← IsKhoOrAdmin, IsKeToanOrAdmin, ...
├── repositories.py         ← Pure ORM, no business logic
├── services.py             ← Business logic, orchestration
├── api_views.py            ← DRF APIView (JSON API)
├── urls.py                 ← /api/inventory/
├── report_urls.py          ← /api/reports/
├── reports/
│   ├── __init__.py
│   ├── base.py             ← BaseReportGenerator (abstract)
│   ├── excel.py            ← Mixin: build_excel() với openpyxl
│   ├── pdf.py              ← Mixin: build_pdf() với weasyprint
│   └── generators/
│       ├── stock_summary.py
│       ├── import_history.py
│       ├── export_history.py
│       ├── loss_report.py
│       ├── discrepancy_report.py
│       └── audit_report.py
├── migrations/
└── tests/
    ├── test_models.py
    ├── test_services.py
    ├── test_api_views.py
    └── test_reports.py
```

---

### 3.2 View → Service → Repository Flow

```
HTTP Request (JWT or Session)
        │
        ▼
[api_views.py — InventoryAuditListCreateView(APIView)]
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsKhoOrKeToanOrAdmin]
        │
        │  Validate via Serializer
        ▼
[services.py — InventoryAuditService]
    create_audit(audit_date, product_ids, user)
        │
        ├──▶ [repositories.py — InventoryAuditRepository]
        │         create_with_snapshot()        ← SELECT + bulk_create, atomic
        │         get_all(), get_by_id()
        │         approve()                     ← adjust stock + create losses
        │
        ├──▶ [warehouse/repositories.py — ProductStockRepository]
        │         select_for_update()           ← prevent race condition
        │         update quantity
        │
        └──▶ [reports/generators/... — StockSummaryExcelReport]
                  build_excel() → bytes
                  as_http_response()

        │
        ▼
[Django HttpResponse / DRF Response]
```

---

### 3.3 Key Code Templates

#### `permissions.py`
```python
from rest_framework.permissions import BasePermission

def _get_role(user):
    return 'ADMIN' if user.is_superuser else getattr(user, 'role', '')

class IsKhoOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return _get_role(request.user) in ('KHO', 'ADMIN')

class IsKeToanOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return _get_role(request.user) in ('KE_TOAN', 'ADMIN')

class IsKhoOrKeToanOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return _get_role(request.user) in ('KHO', 'KE_TOAN', 'ADMIN')
```

#### `repositories.py` (core snippet)
```python
@staticmethod
@transaction.atomic
def create_with_snapshot(audit_data, product_ids, user):
    audit_data['audit_code'] = InventoryAuditRepository.generate_audit_code()
    audit_data['created_by'] = user
    audit_data['status'] = 'DRAFT'
    audit = InventoryAudit.objects.create(**audit_data)

    # Lock rows để tránh race condition
    stocks = ProductStock.objects.select_for_update().filter(
        product_id__in=product_ids
    ).select_related('product')

    items = [
        InventoryAuditItem(
            audit=audit,
            product=stock.product,
            system_quantity=stock.quantity,
            actual_quantity=stock.quantity,  # User sẽ nhập số thực tế
        )
        for stock in stocks
    ]
    InventoryAuditItem.objects.bulk_create(items)
    return audit

@staticmethod
@transaction.atomic
def approve(audit, approved_by):
    audit.status = 'APPROVED'
    audit.approved_by = approved_by
    audit.approved_at = timezone.now()
    audit.save()

    loss_records = []
    for item in audit.items.select_related('product').all():
        # Điều chỉnh stock về số thực tế
        stock, _ = ProductStock.objects.select_for_update().get_or_create(
            product=item.product, defaults={'quantity': 0}
        )
        stock.quantity = item.actual_quantity
        stock.save()

        # Tạo Loss nếu thiếu
        if item.actual_quantity < item.system_quantity:
            loss_records.append(InventoryLoss(
                loss_code=InventoryLossRepository.generate_loss_code(),
                audit_item=item,
                product=item.product,
                loss_quantity=item.system_quantity - item.actual_quantity,
                loss_type='OTHER',
                loss_reason='Phát sinh từ kiểm kê — cần phân loại',
                loss_date=audit.audit_date,
                unit_cost=item.product.base_price,
                status='PENDING',
                created_by=approved_by,
            ))
    if loss_records:
        InventoryLoss.objects.bulk_create(loss_records)
    return audit
```

#### `reports/base.py`
```python
from abc import ABC, abstractmethod
from django.http import HttpResponse
from django.utils import timezone

class BaseReportGenerator(ABC):
    report_type: str = ''
    filename_prefix: str = 'bao-cao'

    def __init__(self, data, filters: dict):
        self.data = data
        self.filters = filters

    @abstractmethod
    def build_excel(self) -> bytes: ...

    @abstractmethod
    def build_pdf(self) -> bytes: ...

    def as_http_response(self, fmt: str) -> HttpResponse:
        date_str = timezone.now().strftime('%Y%m%d')
        if fmt == 'excel':
            content = self.build_excel()
            ct = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            ext = 'xlsx'
        else:
            content = self.build_pdf()
            ct = 'application/pdf'
            ext = 'pdf'
        response = HttpResponse(content, content_type=ct)
        response['Content-Disposition'] = f'attachment; filename="{self.filename_prefix}-{date_str}.{ext}"'
        return response
```

#### `api_views.py` (export endpoint)
```python
class StockSummaryExportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsKeToanOrAdmin]

    def get(self, request):
        fmt = request.query_params.get('format', 'excel')
        if fmt not in ('excel', 'pdf'):
            return Response({'error': 'format phải là excel hoặc pdf'}, status=400)

        stocks = ProductStock.objects.select_related('product__category').all()
        filters = {k: request.query_params.get(k) for k in ('date_from', 'date_to')}

        report = StockSummaryExcelReport(stocks, filters)
        response = report.as_http_response(fmt)

        ReportExportLog.objects.create(
            report_type='STOCK_SUMMARY',
            export_format=fmt.upper(),
            exported_by=request.user,
            filter_params=filters,
            row_count=stocks.count(),
        )
        return response
```

---

## 4. Dependencies to Add

```
# requirements.txt
openpyxl>=3.1.0         # Excel export
weasyprint>=61.0        # PDF export (cần install GTK trên Windows)
```

```python
# settings.py — INSTALLED_APPS
'apps.inventory',
```

```python
# core/urls.py
path('api/inventory/', include('apps.inventory.urls')),
path('api/reports/',   include('apps.inventory.report_urls')),
```

---

## 5. Production Checklist

| Hạng mục | Trước | Sau thiết kế |
|---|---|---|
| Inventory audit model | ❌ | ✅ `InventoryAudit` + `InventoryAuditItem` |
| Loss classification | ❌ | ✅ `InventoryLoss.loss_type` (5 loại) |
| Discrepancy calculation | ❌ | ✅ `InventoryAuditService.get_discrepancy_report()` |
| Export Excel | ❌ | ✅ `BaseReportGenerator` + `openpyxl` |
| Export PDF | ❌ | ✅ `BaseReportGenerator` + `weasyprint` |
| Export audit trail | ❌ | ✅ `ReportExportLog` |
| Race condition on stock | ❌ | ✅ `select_for_update()` + `reserved_quantity` |
| ExportReceipt ↔ SalesOrder FK | ❌ | ✅ `sales_order = ForeignKey(SalesOrder)` |
| Role permissions (DRF) | Partial | ✅ `permissions.py` class riêng |
| DB indexes on filter fields | Partial | ✅ Explicit `indexes` trên mọi filter field |
