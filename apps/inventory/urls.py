from django.urls import path

from .views import (
    InventoryAuditListView,
    InventoryAuditCreateView,
    InventoryAuditDetailView,
    InventoryAuditExportView,
    InventoryLossListView,
    InventoryLossExportView,
    InventoryDiscrepancyView,
    InventoryDiscrepancyExportView,
)

app_name = 'inventory'

urlpatterns = [
    path('inventory/audits/', InventoryAuditListView.as_view(), name='audit_list'),
    path('inventory/audits/create/', InventoryAuditCreateView.as_view(), name='audit_create'),
    path('inventory/audits/<uuid:audit_id>/', InventoryAuditDetailView.as_view(), name='audit_detail'),
    path('inventory/audits/<uuid:audit_id>/export/', InventoryAuditExportView.as_view(), name='audit_export'),
    path('inventory/losses/', InventoryLossListView.as_view(), name='loss_list'),
    path('inventory/losses/export/', InventoryLossExportView.as_view(), name='loss_export'),
    path('inventory/discrepancy/', InventoryDiscrepancyView.as_view(), name='discrepancy_report'),
    path('inventory/discrepancy/export/', InventoryDiscrepancyExportView.as_view(), name='discrepancy_export'),
]
