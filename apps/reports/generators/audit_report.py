from django.utils import timezone

from .base import BaseReportGenerator
from .excel import ExcelTableMixin
from .pdf import PdfTableMixin


class AuditReportGenerator(BaseReportGenerator, ExcelTableMixin, PdfTableMixin):
    report_type = 'AUDIT_REPORT'
    filename_prefix = 'bao-cao-kiem-ke'

    def __init__(self, audit, data, filters=None):
        super().__init__(data=data, filters=filters)
        self.audit = audit

    def _meta(self):
        return [
            f"Audit code: {self.audit.audit_code if self.audit else ''}",
            f"Audit date: {self.audit.audit_date.strftime('%d/%m/%Y') if self.audit and self.audit.audit_date else ''}",
            f"Exported at: {timezone.localtime().strftime('%d/%m/%Y %H:%M:%S')}",
            f"Filters: {self.filters}",
        ]

    def _rows(self):
        rows = []
        for index, item in enumerate(self.data, start=1):
            rows.append([
                index,
                item.product.name,
                float(item.system_quantity),
                float(item.actual_quantity),
                float(item.discrepancy),
                item.note or '',
            ])
        return rows

    def build_excel(self):
        return self.build_excel_table(
            title='BAO CAO KIEM KE',
            headers=['STT', 'San pham', 'So luong he thong', 'So luong thuc te', 'Chenh lech', 'Ghi chu'],
            rows=self._rows(),
            meta=self._meta(),
        )

    def build_pdf(self):
        return self.build_pdf_table(
            title='BAO CAO KIEM KE',
            headers=['STT', 'San pham', 'So luong he thong', 'So luong thuc te', 'Chenh lech', 'Ghi chu'],
            rows=self._rows(),
            meta=self._meta(),
        )
