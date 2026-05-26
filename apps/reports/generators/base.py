from abc import ABC, abstractmethod

from django.http import HttpResponse
from django.utils import timezone


class BaseReportGenerator(ABC):
    report_type = ''
    filename_prefix = 'bao-cao'

    def __init__(self, data, filters=None):
        self.data = data
        self.filters = filters or {}

    @abstractmethod
    def build_excel(self):
        raise NotImplementedError

    @abstractmethod
    def build_pdf(self):
        raise NotImplementedError

    def as_http_response(self, fmt):
        fmt = (fmt or 'excel').lower()
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')

        if fmt == 'excel':
            content = self.build_excel()
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            ext = 'xlsx'
        elif fmt == 'pdf':
            content = self.build_pdf()
            content_type = 'application/pdf'
            ext = 'pdf'
        else:
            raise ValueError('Unsupported format')

        response = HttpResponse(content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{self.filename_prefix}-{timestamp}.{ext}"'
        return response
