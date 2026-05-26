"""Report export API routes."""

from django.urls import path

from .api_views import (
    StockSummaryExportView,
    ImportHistoryExportView,
    ExportHistoryExportView,
    LossReportExportView,
    DiscrepancyExportView,
    AuditReportExportView,
    DiscrepancyReportView,
    LossReportView,
)

app_name = 'reports_api'

urlpatterns = [
    path('stock-summary/export/', StockSummaryExportView.as_view(), name='stock-summary-export'),
    path('import-history/export/', ImportHistoryExportView.as_view(), name='import-history-export'),
    path('export-history/export/', ExportHistoryExportView.as_view(), name='export-history-export'),
    path('loss-report/export/', LossReportExportView.as_view(), name='loss-report-export'),
    path('discrepancy/export/', DiscrepancyExportView.as_view(), name='discrepancy-export'),
    path('audit-report/export/', AuditReportExportView.as_view(), name='audit-report-export'),
    path('discrepancy/data/', DiscrepancyReportView.as_view(), name='discrepancy-data'),
    path('loss-report/data/', LossReportView.as_view(), name='loss-report-data'),
]
