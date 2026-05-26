from decimal import Decimal
from django.utils import timezone
from django.db.models import Sum

from apps.product.models import Category, Product
from apps.warehouse.models import ImportReceiptItem, ExportReceiptItem
from apps.inventory.models import InventoryLoss, InventoryAudit
from apps.order.models import SalesOrder, SalesOrderItem

# Import internal
from .repositories import ReportRepository

class StockReportService:
    """Báo cáo tồn kho theo thời gian (US-23)."""

    @staticmethod
    def get_categories():
        return Category.objects.all().order_by('name')

    @staticmethod
    def _apply_export(balance, quantity):
        # Đồng bộ với logic kho hiện tại: không để âm tồn.
        updated = balance - quantity
        return updated if updated > 0 else Decimal('0')

    def build_report(self, from_date, to_date, category_id=None):
        products_qs = Product.objects.select_related('category').all().order_by('name')
        if category_id:
            products_qs = products_qs.filter(category_id=category_id)

        products = list(products_qs)
        if not products:
            zero = Decimal('0')
            return [], {
                'opening': zero,
                'import_qty': zero,
                'export_qty': zero,
                'closing': zero,
            }

        product_ids = [p.id for p in products]

        report_map = {}
        balances = {}
        for product in products:
            report_map[product.id] = {
                'product': product,
                'opening': Decimal('0'),
                'import_qty': Decimal('0'),
                'export_qty': Decimal('0'),
                'closing': Decimal('0'),
            }
            balances[product.id] = Decimal('0')

        import_items = ImportReceiptItem.objects.filter(
            product_id__in=product_ids,
            receipt__status='APPROVED',
            receipt__reviewed_at__date__lte=to_date,
        ).values('product_id', 'quantity', 'receipt__reviewed_at')

        export_items = ExportReceiptItem.objects.filter(
            product_id__in=product_ids,
            receipt__status='APPROVED',
            receipt__reviewed_at__date__lte=to_date,
        ).values('product_id', 'quantity', 'receipt__reviewed_at')

        pre_period_events = []
        in_period_events = []

        for row in import_items:
            event_date = row['receipt__reviewed_at'].date()
            event = (row['receipt__reviewed_at'], row['product_id'], Decimal(str(row['quantity'])), 'IMPORT')
            if event_date < from_date:
                pre_period_events.append(event)
            else:
                in_period_events.append(event)

        for row in export_items:
            event_date = row['receipt__reviewed_at'].date()
            event = (row['receipt__reviewed_at'], row['product_id'], Decimal(str(row['quantity'])), 'EXPORT')
            if event_date < from_date:
                pre_period_events.append(event)
            else:
                in_period_events.append(event)

        pre_period_events.sort(key=lambda x: (x[0], 0 if x[3] == 'IMPORT' else 1))
        in_period_events.sort(key=lambda x: (x[0], 0 if x[3] == 'IMPORT' else 1))

        # Tính tồn đầu kỳ bằng cách replay các giao dịch trước kỳ.
        for _, product_id, quantity, event_type in pre_period_events:
            if event_type == 'IMPORT':
                balances[product_id] += quantity
            else:
                balances[product_id] = self._apply_export(balances[product_id], quantity)

        for product_id, row in report_map.items():
            row['opening'] = balances[product_id]

        # Tính nhập/xuất trong kỳ và tồn cuối kỳ.
        for reviewed_at, product_id, quantity, event_type in in_period_events:
            event_date = reviewed_at.date()
            if event_date > to_date:
                continue

            if event_type == 'IMPORT':
                report_map[product_id]['import_qty'] += quantity
                balances[product_id] += quantity
            else:
                report_map[product_id]['export_qty'] += quantity
                balances[product_id] = self._apply_export(balances[product_id], quantity)

        for product_id, row in report_map.items():
            row['closing'] = balances[product_id]

        rows = [report_map[product.id] for product in products]

        totals = {
            'opening': sum((row['opening'] for row in rows), Decimal('0')),
            'import_qty': sum((row['import_qty'] for row in rows), Decimal('0')),
            'export_qty': sum((row['export_qty'] for row in rows), Decimal('0')),
            'closing': sum((row['closing'] for row in rows), Decimal('0')),
        }
        return rows, totals


class LossReportService:
    """Service for discrepancy and report summary payloads."""

    @staticmethod
    def generate_loss_report(date_from=None, date_to=None):
        summary = ReportRepository.get_report_summary(date_from=date_from, date_to=date_to)
        aggregations = list(ReportRepository.aggregate_loss_by_type(date_from=date_from, date_to=date_to))

        total_value = summary['total_loss_value'] or Decimal('0.00')
        result = []
        for agg in aggregations:
            agg_value = agg['total_value'] or Decimal('0.00')
            if total_value > 0:
                percentage = round((agg_value / total_value) * 100, 2)
            else:
                percentage = Decimal('0.00')

            result.append({
                **agg,
                'percentage_of_total_cost': percentage,
                'type_label': dict(InventoryLoss.LossType.choices).get(agg['loss_type'], 'Khac'),
            })

        return {
            'overall_summary': {
                'total_audits_passed': summary['total_approved_audits'],
                'total_impact_value': total_value,
            },
            'breakdown_by_type': result,
        }

    @staticmethod
    def generate_discrepancy_report(product_id=None, category_id=None):
        rows = ReportRepository.discrepancy_rows(product_id=product_id, category_id=category_id)

        payload_rows = []
        shortage_count = 0
        surplus_count = 0
        ok_count = 0

        for row in rows:
            discrepancy = row['discrepancy']
            if discrepancy is None:
                status = 'NO_AUDIT'
            elif discrepancy < 0:
                status = 'SHORTAGE'
                shortage_count += 1
            elif discrepancy > 0:
                status = 'SURPLUS'
                surplus_count += 1
            else:
                status = 'MATCH'
                ok_count += 1

            payload_rows.append({
                'product_id': row['product'].id,
                'product_name': row['product'].name,
                'system_quantity': row['system_quantity'],
                'reserved_quantity': row['reserved_quantity'],
                'available_quantity': row['available_quantity'],
                'last_audit_date': row['last_audit_date'],
                'last_actual_qty': row['last_actual_qty'],
                'discrepancy': discrepancy,
                'discrepancy_pct': row['discrepancy_pct'],
                'status': status,
            })

        return {
            'generated_at': timezone.localtime(),
            'items': payload_rows,
            'summary': {
                'shortage_count': shortage_count,
                'surplus_count': surplus_count,
                'ok_count': ok_count,
            },
        }


class OrderReportService:
    @staticmethod
    def get_sales_order_stats():
        today = timezone.now().date()
        return {
            'total_orders': SalesOrder.objects.count(),
            'pending_orders': SalesOrder.objects.filter(status='WAITING').count(),
            'total_items': SalesOrderItem.objects.aggregate(total=Sum('quantity'))['total'] or 0,
            'today_transactions': SalesOrder.objects.filter(created_at__date=today).count(),
        }
