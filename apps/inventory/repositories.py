"""
Data-access layer for inventory audits, loss records, and report exports.
"""

from decimal import Decimal

from django.db import transaction
from django.db.models import DecimalField, F, Sum, Count
from django.db.models.functions import Coalesce, TruncMonth
from django.utils import timezone

from apps.warehouse.models import ProductStock

from .models import InventoryAudit, InventoryAuditItem, InventoryLoss


class InventoryRepository:
    """Repository for InventoryAudit and InventoryAuditItem."""

    @staticmethod
    def generate_audit_code():
        date_str = timezone.now().strftime('%Y%m%d')
        count = InventoryAudit.objects.filter(audit_code__startswith=f'KK-{date_str}').count() + 1
        return f'KK-{date_str}-{count:03d}'

    @staticmethod
    def list_checks(status=None, search=None, date_from=None, date_to=None):
        qs = InventoryAudit.objects.select_related(
            'created_by', 'approved_by'
        ).prefetch_related('items__product__category')

        if status:
            qs = qs.filter(status=status)
        if search:
            qs = qs.filter(audit_code__icontains=search)
        if date_from:
            qs = qs.filter(audit_date__gte=date_from)
        if date_to:
            qs = qs.filter(audit_date__lte=date_to)

        return qs.order_by('-audit_date', '-created_at')

    @staticmethod
    def get_by_id(check_id):
        try:
            return InventoryAudit.objects.select_related(
                'created_by', 'approved_by'
            ).prefetch_related('items__product__category').get(id=check_id)
        except InventoryAudit.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def create_check(audit_date, note, product_ids, user):
        audit = InventoryAudit.objects.create(
            audit_code=InventoryRepository.generate_audit_code(),
            audit_date=audit_date,
            note=note or '',
            status=InventoryAudit.Status.DRAFT,
            created_by=user,
        )

        stocks = ProductStock.objects.select_for_update().filter(
            product_id__in=product_ids
        ).select_related('product')
        stock_map = {str(stock.product_id): stock.quantity for stock in stocks}

        items = []
        for product_id in product_ids:
            system_qty = stock_map.get(str(product_id), Decimal('0'))
            items.append(
                InventoryAuditItem(
                    audit=audit,
                    product_id=product_id,
                    system_quantity=system_qty,
                    actual_quantity=system_qty,
                )
            )

        InventoryAuditItem.objects.bulk_create(items, ignore_conflicts=True)
        return audit

    @staticmethod
    def get_item(check_id, item_id):
        try:
            return InventoryAuditItem.objects.select_related('audit', 'product').get(
                id=item_id,
                audit_id=check_id,
            )
        except InventoryAuditItem.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def update_item(audit, item_id, actual_quantity, note=''):
        item = InventoryRepository.get_item(audit.id, item_id)
        if item is None:
            return None

        item.actual_quantity = actual_quantity
        item.note = note or ''
        item.save(update_fields=['actual_quantity', 'note', 'updated_at'])
        return item

    @staticmethod
    def submit_check(audit):
        audit.status = InventoryAudit.Status.SUBMITTED
        audit.rejection_note = ''
        audit.save(update_fields=['status', 'rejection_note', 'updated_at'])
        return audit

    @staticmethod
    def cancel_check(audit, cancel_note=''):
        audit.status = InventoryAudit.Status.CANCELLED
        audit.rejection_note = cancel_note or ''
        audit.save(update_fields=['status', 'rejection_note', 'updated_at'])
        return audit

    @staticmethod
    def get_discrepancy(check_id):
        return InventoryAuditItem.objects.filter(audit_id=check_id).annotate(
            calculated_discrepancy=F('actual_quantity') - F('system_quantity')
        ).values(
            'id',
            'product_id',
            'product__name',
            'system_quantity',
            'actual_quantity',
            'calculated_discrepancy',
            'note',
        )

    @staticmethod
    @transaction.atomic
    def approve_check(audit, approved_by):
        audit.status = InventoryAudit.Status.APPROVED
        audit.approved_by = approved_by
        audit.approved_at = timezone.now()
        audit.rejection_note = ''
        audit.save(update_fields=['status', 'approved_by', 'approved_at', 'rejection_note', 'updated_at'])

        items = audit.items.select_related('product').all()
        for item in items:
            stock, _ = ProductStock.objects.select_for_update().get_or_create(
                product=item.product,
                defaults={'quantity': 0, 'reserved_quantity': 0},
            )
            stock.quantity = item.actual_quantity
            if stock.reserved_quantity > stock.quantity:
                stock.reserved_quantity = stock.quantity
            stock.save(update_fields=['quantity', 'reserved_quantity', 'last_updated'])

            if item.actual_quantity < item.system_quantity:
                shortage = item.system_quantity - item.actual_quantity
                LossRepository.create_loss(
                    product_id=item.product_id,
                    loss_quantity=shortage,
                    loss_type=InventoryLoss.LossType.OTHER,
                    loss_reason='Phat sinh tu kiem ke - can phan loai',
                    loss_date=audit.audit_date,
                    unit_cost=item.product.base_price,
                    user=approved_by,
                    audit_item=item,
                    status=InventoryLoss.Status.PENDING,
                )

        return audit


class LossRepository:
    """Repository for InventoryLoss workflows and statistics."""

    @staticmethod
    def generate_loss_code():
        date_str = timezone.now().strftime('%Y%m%d')
        count = InventoryLoss.objects.filter(loss_code__startswith=f'HH-{date_str}').count() + 1
        return f'HH-{date_str}-{count:03d}'

    @staticmethod
    def list_losses(loss_type=None, status=None, date_from=None, date_to=None, product_id=None, search=None):
        qs = InventoryLoss.objects.select_related(
            'product__category', 'audit_item__audit', 'created_by', 'reviewed_by'
        )

        if loss_type:
            qs = qs.filter(loss_type=loss_type)
        if status:
            qs = qs.filter(status=status)
        if date_from:
            qs = qs.filter(loss_date__gte=date_from)
        if date_to:
            qs = qs.filter(loss_date__lte=date_to)
        if product_id:
            qs = qs.filter(product_id=product_id)
        if search:
            qs = qs.filter(loss_code__icontains=search)

        return qs.order_by('-loss_date', '-created_at')

    @staticmethod
    def get_by_id(loss_id):
        try:
            return InventoryLoss.objects.select_related(
                'product__category', 'audit_item__audit', 'created_by', 'reviewed_by'
            ).get(id=loss_id)
        except InventoryLoss.DoesNotExist:
            return None

    @staticmethod
    def get_by_check_id(check_id):
        return InventoryLoss.objects.select_related(
            'product__category', 'created_by', 'reviewed_by'
        ).filter(audit_item__audit_id=check_id)

    @staticmethod
    @transaction.atomic
    def create_loss(
        product_id,
        loss_quantity,
        loss_type,
        loss_reason,
        loss_date,
        unit_cost,
        user,
        audit_item=None,
        status=InventoryLoss.Status.PENDING,
    ):
        return InventoryLoss.objects.create(
            loss_code=LossRepository.generate_loss_code(),
            audit_item=audit_item,
            product_id=product_id,
            loss_quantity=loss_quantity,
            loss_type=loss_type,
            loss_reason=loss_reason,
            loss_date=loss_date,
            unit_cost=unit_cost,
            status=status,
            created_by=user,
        )

    @staticmethod
    def update_loss(loss, loss_type=None, loss_reason=None):
        update_fields = ['updated_at']

        if loss_type is not None:
            loss.loss_type = loss_type
            update_fields.append('loss_type')
        if loss_reason is not None:
            loss.loss_reason = loss_reason
            update_fields.append('loss_reason')

        loss.save(update_fields=update_fields)
        return loss

    @staticmethod
    @transaction.atomic
    def approve_loss(loss, reviewed_by):
        loss.status = InventoryLoss.Status.APPROVED
        loss.reviewed_by = reviewed_by
        loss.reviewed_at = timezone.now()
        loss.rejection_note = ''
        loss.save(update_fields=['status', 'reviewed_by', 'reviewed_at', 'rejection_note', 'updated_at'])

        # Chỉ trừ kho đối với phiếu hao hụt tạo thủ công (không liên kết với phiên kiểm kê).
        # Phiếu sinh ra từ kiểm kê thì số tồn trên hệ thống đã được cập nhật thành số thực tế lúc duyệt phiên kiểm kê.
        if loss.audit_item_id is None:
            stock, _ = ProductStock.objects.select_for_update().get_or_create(
                product=loss.product,
                defaults={'quantity': 0, 'reserved_quantity': 0},
            )
            stock.quantity -= loss.loss_quantity
            if stock.quantity < 0:
                stock.quantity = 0
            if stock.reserved_quantity > stock.quantity:
                stock.reserved_quantity = stock.quantity
            stock.save(update_fields=['quantity', 'reserved_quantity', 'last_updated'])

        return loss

    @staticmethod
    def reject_loss(loss, reviewed_by, rejection_note):
        loss.status = InventoryLoss.Status.REJECTED
        loss.reviewed_by = reviewed_by
        loss.reviewed_at = timezone.now()
        loss.rejection_note = rejection_note
        loss.save(update_fields=['status', 'reviewed_by', 'reviewed_at', 'rejection_note', 'updated_at'])
        return loss

    @staticmethod
    def _filtered_loss_queryset(date_from=None, date_to=None, loss_type=None, product_id=None):
        qs = InventoryLoss.objects.filter(status=InventoryLoss.Status.APPROVED)

        if date_from:
            qs = qs.filter(loss_date__gte=date_from)
        if date_to:
            qs = qs.filter(loss_date__lte=date_to)
        if loss_type:
            qs = qs.filter(loss_type=loss_type)
        if product_id:
            qs = qs.filter(product_id=product_id)

        return qs

    @staticmethod
    def aggregate_by_type(date_from=None, date_to=None, loss_type=None, product_id=None):
        qs = LossRepository._filtered_loss_queryset(
            date_from=date_from,
            date_to=date_to,
            loss_type=loss_type,
            product_id=product_id,
        )

        return qs.values('loss_type').annotate(
            count=Count('id'),
            total_quantity=Coalesce(Sum('loss_quantity'), 0, output_field=DecimalField(max_digits=15, decimal_places=2)),
            total_value=Coalesce(
                Sum(F('loss_quantity') * F('unit_cost'), output_field=DecimalField(max_digits=19, decimal_places=4)),
                0,
                output_field=DecimalField(max_digits=19, decimal_places=4),
            ),
        ).order_by('-total_value')

    @staticmethod
    def aggregate_by_month(date_from=None, date_to=None, loss_type=None, product_id=None):
        qs = LossRepository._filtered_loss_queryset(
            date_from=date_from,
            date_to=date_to,
            loss_type=loss_type,
            product_id=product_id,
        )

        return qs.annotate(month=TruncMonth('loss_date')).values('month').annotate(
            total_quantity=Coalesce(Sum('loss_quantity'), 0, output_field=DecimalField(max_digits=15, decimal_places=2)),
            total_value=Coalesce(
                Sum(F('loss_quantity') * F('unit_cost'), output_field=DecimalField(max_digits=19, decimal_places=4)),
                0,
                output_field=DecimalField(max_digits=19, decimal_places=4),
            ),
        ).order_by('-month')

    @staticmethod
    def top_products(date_from=None, date_to=None, loss_type=None, product_id=None, limit=10):
        qs = LossRepository._filtered_loss_queryset(
            date_from=date_from,
            date_to=date_to,
            loss_type=loss_type,
            product_id=product_id,
        )

        return qs.values('product_id', 'product__name').annotate(
            total_quantity=Coalesce(Sum('loss_quantity'), 0, output_field=DecimalField(max_digits=15, decimal_places=2)),
            total_value=Coalesce(
                Sum(F('loss_quantity') * F('unit_cost'), output_field=DecimalField(max_digits=19, decimal_places=4)),
                0,
                output_field=DecimalField(max_digits=19, decimal_places=4),
            ),
        ).order_by('-total_value')[:limit]



