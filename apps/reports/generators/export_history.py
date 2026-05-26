from django.utils import timezone

from .base import BaseReportGenerator
from .excel import ExcelTableMixin
from .pdf import PdfTableMixin


class ExportHistoryReportGenerator(BaseReportGenerator, ExcelTableMixin, PdfTableMixin):
    report_type = 'EXPORT_HISTORY'
    filename_prefix = 'lich-su-xuat-kho'

    def _meta(self):
        return [
            f"Exported at: {timezone.localtime().strftime('%d/%m/%Y %H:%M:%S')}",
            f"Filters: {self.filters}",
        ]

    def _rows(self):
        rows = []
        for index, item in enumerate(self.data, start=1):
            order_code = item.receipt.sales_order.order_code if item.receipt.sales_order else ''
            rows.append([
                index,
                item.receipt.receipt_code,
                order_code,
                item.product.name,
                float(item.quantity),
                float(item.unit_price),
                item.receipt.reviewed_at.strftime('%d/%m/%Y %H:%M') if item.receipt.reviewed_at else '',
            ])
        return rows

    def build_excel(self):
        return self.build_excel_table(
            title='LICH SU XUAT KHO',
            headers=['STT', 'Ma phieu', 'Ma don', 'San pham', 'So luong', 'Don gia', 'Ngay duyet'],
            rows=self._rows(),
            meta=self._meta(),
        )

    def build_pdf(self):
        return self.build_pdf_table(
            title='LICH SU XUAT KHO',
            headers=['STT', 'Ma phieu', 'Ma don', 'San pham', 'So luong', 'Don gia', 'Ngay duyet'],
            rows=self._rows(),
            meta=self._meta(),
        )
