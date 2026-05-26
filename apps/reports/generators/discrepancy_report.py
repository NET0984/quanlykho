from django.utils import timezone

from .base import BaseReportGenerator
from .excel import ExcelTableMixin
from .pdf import PdfTableMixin


class DiscrepancyReportGenerator(BaseReportGenerator, ExcelTableMixin, PdfTableMixin):
    report_type = 'DISCREPANCY'
    filename_prefix = 'bao-cao-chenh-lech'

    def _meta(self):
        return [
            f"Exported at: {timezone.localtime().strftime('%d/%m/%Y %H:%M:%S')}",
            f"Filters: {self.filters}",
        ]

    def _rows(self):
        rows = []
        for index, row in enumerate(self.data, start=1):
            discrepancy = row['discrepancy']
            if discrepancy is None:
                status_label = 'Chua kiem ke'
            elif discrepancy < 0:
                status_label = 'Thieu'
            elif discrepancy > 0:
                status_label = 'Thua'
            else:
                status_label = 'Khop'

            rows.append([
                index,
                row['product'].name,
                float(row['system_quantity']),
                float(row['reserved_quantity']),
                float(row['available_quantity']),
                float(row['last_actual_qty']) if row['last_actual_qty'] is not None else '',
                float(discrepancy) if discrepancy is not None else '',
                status_label,
            ])
        return rows

    def build_excel(self):
        return self.build_excel_table(
            title='BAO CAO CHENH LECH KHO',
            headers=['STT', 'San pham', 'Ton he thong', 'Dang giu', 'Kha dung', 'Thuc te gan nhat', 'Chenh lech', 'Trang thai'],
            rows=self._rows(),
            meta=self._meta(),
        )

    def build_pdf(self):
        return self.build_pdf_table(
            title='BAO CAO CHENH LECH KHO',
            headers=['STT', 'San pham', 'Ton he thong', 'Dang giu', 'Kha dung', 'Thuc te gan nhat', 'Chenh lech', 'Trang thai'],
            rows=self._rows(),
            meta=self._meta(),
        )
