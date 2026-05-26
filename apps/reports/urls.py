from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Báo cáo tồn kho
    path('stock/', views.StockReportView.as_view(), name='stock_report'),
    path('stock/export-excel/', views.StockReportExportExcelView.as_view(), name='stock_report_export_excel'),
    path('stock/export-pdf/', views.StockReportExportPdfView.as_view(), name='stock_report_export_pdf'),

    # Báo cáo đơn hàng (xuất file)
    path('sales/export-excel/', views.SalesOrderExportExcelView.as_view(), name='sales_export_excel'),
    path('sales/export-pdf/', views.SalesOrderExportPdfView.as_view(), name='sales_export_pdf'),
]
