from django.utils import timezone

from .base import BaseReportGenerator
from .excel import ExcelTableMixin
from .pdf import PdfTableMixin


class StockSummaryReportGenerator(BaseReportGenerator, ExcelTableMixin, PdfTableMixin):
    report_type = 'STOCK_SUMMARY'
    filename_prefix = 'bao-cao-ton-kho'

    def _meta(self):
        return [
            f"Exported at: {timezone.localtime().strftime('%d/%m/%Y %H:%M:%S')}",
            f"Filters: {self.filters}",
        ]

    def _rows(self):
        rows = []
        for index, stock in enumerate(self.data, start=1):
            rows.append([
                index,
                stock.product.name,
                stock.product.category.name if stock.product.category else '',
                float(stock.quantity),
                float(stock.reserved_quantity),
                float(stock.available_quantity),
            ])
        return rows

    def build_excel(self):
        return self.build_excel_table(
            title='BAO CAO TONG HOP TON KHO',
            headers=['STT', 'San pham', 'Danh muc', 'Ton he thong', 'Dang giu', 'Kha dung'],
            rows=self._rows(),
            meta=self._meta(),
        )

    def build_pdf(self):
        return self.build_pdf_table(
            title='BAO CAO TONG HOP TON KHO',
            headers=['STT', 'San pham', 'Danh muc', 'Ton he thong', 'Dang giu', 'Kha dung'],
            rows=self._rows(),
            meta=self._meta(),
        )
