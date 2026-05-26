from django.utils import timezone

from .base import BaseReportGenerator
from .excel import ExcelTableMixin
from .pdf import PdfTableMixin


class LossReportGenerator(BaseReportGenerator, ExcelTableMixin, PdfTableMixin):
    report_type = 'LOSS_REPORT'
    filename_prefix = 'bao-cao-hao-hut'

    def _meta(self):
        return [
            f"Exported at: {timezone.localtime().strftime('%d/%m/%Y %H:%M:%S')}",
            f"Filters: {self.filters}",
        ]

    def _rows(self):
        rows = []
        for index, loss in enumerate(self.data, start=1):
            rows.append([
                index,
                loss.loss_code,
                loss.product.name,
                loss.get_loss_type_display(),
                float(loss.loss_quantity),
                float(loss.unit_cost),
                float(loss.total_loss_value),
                loss.get_status_display(),
                loss.loss_date.strftime('%d/%m/%Y') if loss.loss_date else '',
            ])
        return rows

    def build_excel(self):
        return self.build_excel_table(
            title='BAO CAO HAO HUT',
            headers=['STT', 'Ma phieu', 'San pham', 'Loai hao hut', 'So luong', 'Don gia', 'Gia tri', 'Trang thai', 'Ngay hao hut'],
            rows=self._rows(),
            meta=self._meta(),
        )

    def build_pdf(self):
        return self.build_pdf_table(
            title='BAO CAO HAO HUT',
            headers=['STT', 'Ma phieu', 'San pham', 'Loai hao hut', 'So luong', 'Don gia', 'Gia tri', 'Trang thai', 'Ngay hao hut'],
            rows=self._rows(),
            meta=self._meta(),
        )
