from django.urls import path
from . import views

app_name = 'warehouse'

urlpatterns = [
    path('import/', views.ImportReceiptListView.as_view(), name='import_list'),
    path('import/excel/template/', views.ImportReceiptExcelTemplateView.as_view(), name='import_excel_template'),
    path('import/excel/upload/', views.ImportReceiptExcelUploadView.as_view(), name='import_excel_upload'),
    path('import/excel/export/', views.ImportReceiptExcelExportView.as_view(), name='import_excel_export'),
    path('import/<uuid:pk>/', views.ImportReceiptDetailView.as_view(), name='import_detail'),
    path('import/<uuid:pk>/approve/', views.ImportReceiptApproveView.as_view(), name='import_approve'),
    path('import/<uuid:pk>/reject/', views.ImportReceiptRejectView.as_view(), name='import_reject'),
    path('import/<uuid:pk>/resubmit/', views.ImportReceiptResubmitView.as_view(), name='import_resubmit'),

    path('export/', views.ExportReceiptListView.as_view(), name='export_list'),
    path('export/excel/template/', views.ExportReceiptExcelTemplateView.as_view(), name='export_excel_template'),
    path('export/excel/upload/', views.ExportReceiptExcelUploadView.as_view(), name='export_excel_upload'),
    path('export/excel/export/', views.ExportReceiptExcelExportView.as_view(), name='export_excel_export'),
    path('export/<uuid:pk>/', views.ExportReceiptDetailView.as_view(), name='export_detail'),
    path('export/<uuid:pk>/mark-picked/', views.ExportReceiptMarkPickedView.as_view(), name='export_mark_picked'),
    path('export/<uuid:pk>/approve/', views.ExportReceiptApproveView.as_view(), name='export_approve'),
    path('export/<uuid:pk>/reject/', views.ExportReceiptRejectView.as_view(), name='export_reject'),
    path('export/<uuid:pk>/resubmit/', views.ExportReceiptResubmitView.as_view(), name='export_resubmit'),

    path('stock/', views.StockListView.as_view(), name='stock_list'),
]
