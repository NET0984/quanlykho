import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class ReportExportLog(models.Model):
    """
    Ghi lại mọi lần xuất báo cáo.
    Dùng cho audit trail: ai xuất, lúc nào, bao nhiêu dòng,
    tham số lọc nào được dùng.
    """

    class ExportFormat(models.TextChoices):
        EXCEL = 'EXCEL', _('Excel (.xlsx)')
        PDF   = 'PDF',   _('PDF')

    class ReportType(models.TextChoices):
        STOCK_SUMMARY  = 'STOCK_SUMMARY',  _('Tổng hợp tồn kho')
        IMPORT_HISTORY = 'IMPORT_HISTORY', _('Lịch sử nhập kho')
        EXPORT_HISTORY = 'EXPORT_HISTORY', _('Lịch sử xuất kho')
        LOSS_REPORT    = 'LOSS_REPORT',    _('Báo cáo hao hụt')
        AUDIT_REPORT   = 'AUDIT_REPORT',   _('Báo cáo kiểm kê')
        DISCREPANCY    = 'DISCREPANCY',    _('Báo cáo chênh lệch kho')

    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report_type   = models.CharField(max_length=20, choices=ReportType.choices, db_index=True)
    export_format = models.CharField(max_length=5, choices=ExportFormat.choices)
    exported_by   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='report_exports',
    )
    exported_at   = models.DateTimeField(auto_now_add=True, db_index=True)
    # Lưu toàn bộ query params dưới dạng JSON → dễ replay / debug
    filter_params = models.JSONField(default=dict, blank=True)
    row_count     = models.IntegerField(default=0)

    class Meta:
        db_table = 'report_export_logs'
        ordering = ['-exported_at']
        indexes  = [
            models.Index(fields=['report_type', 'exported_at'], name='idx_exportlog_type_date'),
            models.Index(fields=['exported_by'],                name='idx_exportlog_user'),
        ]
        verbose_name        = _('Nhật ký xuất báo cáo')
        verbose_name_plural = _('Nhật ký xuất báo cáo')

    def __str__(self):
        return (
            f'{self.get_report_type_display()} | '
            f'{self.export_format} | '
            f'{self.exported_by} | '
            f'{self.exported_at:%Y-%m-%d %H:%M}'
        )
