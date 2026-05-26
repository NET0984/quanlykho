from decimal import Decimal
from django.db.models import DecimalField, F, Sum
from django.db.models.functions import Coalesce
from apps.product.models import Product
from apps.warehouse.models import ProductStock, ImportReceiptItem, ExportReceiptItem
from apps.inventory.models import InventoryAudit, InventoryAuditItem, InventoryLoss
from .models import ReportExportLog
from apps.inventory.repositories import LossRepository, InventoryRepository

class ReportRepository:
    """Repository for report data retrieval and export logging."""

    @staticmethod
    def log_export(report_type, export_format, exported_by, filter_params=None, row_count=0):
        return ReportExportLog.objects.create(
            report_type=report_type,
            export_format=export_format,
            exported_by=exported_by,
            filter_params=filter_params or {},
            row_count=row_count,
        )

    @staticmethod
    def get_report_summary(date_from=None, date_to=None):
        audit_qs = InventoryAudit.objects.filter(status=InventoryAudit.Status.APPROVED)
        loss_qs = InventoryLoss.objects.filter(status=InventoryLoss.Status.APPROVED)

        if date_from:
            audit_qs = audit_qs.filter(audit_date__gte=date_from)
            loss_qs = loss_qs.filter(loss_date__gte=date_from)
        if date_to:
            audit_qs = audit_qs.filter(audit_date__lte=date_to)
            loss_qs = loss_qs.filter(loss_date__lte=date_to)

        total_loss_value = loss_qs.aggregate(
            total=Coalesce(
                Sum(F('loss_quantity') * F('unit_cost'), output_field=DecimalField(max_digits=19, decimal_places=4)),
                0,
                output_field=DecimalField(max_digits=19, decimal_places=4),
            )
        )['total']

        return {
            'total_approved_audits': audit_qs.count(),
            'total_loss_value': total_loss_value,
        }

    @staticmethod
    def aggregate_loss_by_type(date_from=None, date_to=None):
        return LossRepository.aggregate_by_type(date_from=date_from, date_to=date_to)

    @staticmethod
    def stock_summary_rows(category_id=None):
        qs = ProductStock.objects.select_related('product__category').all().order_by('product__name')
        if category_id:
            qs = qs.filter(product__category_id=category_id)
        return qs

    @staticmethod
    def import_history_rows(date_from=None, date_to=None):
        qs = ImportReceiptItem.objects.select_related(
            'receipt', 'product__category', 'receipt__created_by', 'receipt__reviewed_by'
        ).filter(receipt__status='APPROVED').order_by('-receipt__reviewed_at', '-receipt__created_at')

        if date_from:
            qs = qs.filter(receipt__reviewed_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(receipt__reviewed_at__date__lte=date_to)

        return qs

    @staticmethod
    def export_history_rows(date_from=None, date_to=None):
        qs = ExportReceiptItem.objects.select_related(
            'receipt', 'product__category', 'receipt__created_by', 'receipt__reviewed_by', 'receipt__sales_order'
        ).filter(receipt__status='APPROVED').order_by('-receipt__reviewed_at', '-receipt__created_at')

        if date_from:
            qs = qs.filter(receipt__reviewed_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(receipt__reviewed_at__date__lte=date_to)

        return qs

    @staticmethod
    def loss_report_rows(date_from=None, date_to=None, loss_type=None):
        qs = InventoryLoss.objects.select_related('product__category', 'created_by', 'reviewed_by').all()

        if date_from:
            qs = qs.filter(loss_date__gte=date_from)
        if date_to:
            qs = qs.filter(loss_date__lte=date_to)
        if loss_type:
            qs = qs.filter(loss_type=loss_type)

        return qs.order_by('-loss_date', '-created_at')

    @staticmethod
    def discrepancy_rows(product_id=None, category_id=None):
        products_qs = Product.objects.select_related('category').all().order_by('name')
        if product_id:
            products_qs = products_qs.filter(id=product_id)
        if category_id:
            products_qs = products_qs.filter(category_id=category_id)

        products = list(products_qs)
        if not products:
            return []

        product_ids = [product.id for product in products]

        stock_map = {
            stock.product_id: stock
            for stock in ProductStock.objects.filter(product_id__in=product_ids).select_related('product')
        }

        latest_items = InventoryAuditItem.objects.select_related('audit').filter(
            product_id__in=product_ids,
            audit__status=InventoryAudit.Status.APPROVED,
        ).order_by('product_id', '-audit__audit_date', '-audit__created_at')

        latest_item_map = {}
        for item in latest_items:
            if item.product_id not in latest_item_map:
                latest_item_map[item.product_id] = item

        rows = []
        for product in products:
            stock = stock_map.get(product.id)
            system_quantity = stock.quantity if stock else Decimal('0')
            reserved_quantity = stock.reserved_quantity if stock else Decimal('0')
            latest_item = latest_item_map.get(product.id)

            if latest_item:
                last_actual_qty = latest_item.actual_quantity
                last_audit_date = latest_item.audit.audit_date
                discrepancy = last_actual_qty - system_quantity
                discrepancy_pct = None
                if system_quantity > 0:
                    discrepancy_pct = round((discrepancy / system_quantity) * 100, 2)
            else:
                last_actual_qty = None
                last_audit_date = None
                discrepancy = None
                discrepancy_pct = None

            rows.append({
                'product': product,
                'system_quantity': system_quantity,
                'reserved_quantity': reserved_quantity,
                'available_quantity': system_quantity - reserved_quantity,
                'last_actual_qty': last_actual_qty,
                'last_audit_date': last_audit_date,
                'discrepancy': discrepancy,
                'discrepancy_pct': discrepancy_pct,
            })

        return rows

    @staticmethod
    def audit_report_rows(audit_id):
        audit = InventoryRepository.get_by_id(audit_id)
        if audit is None:
            return None, []

        rows = list(audit.items.select_related('product__category').all())
        return audit, rows
