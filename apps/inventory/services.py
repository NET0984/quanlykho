"""
Business logic layer for inventory workflows.
"""

from decimal import Decimal

from django.core.exceptions import ValidationError
from apps.product.models import Product

from .models import InventoryAudit, InventoryLoss
from .repositories import InventoryRepository, LossRepository


class InventoryService:
    """Service handling business rules for InventoryAudit workflows."""

    @staticmethod
    def list_checks(status=None, search=None, date_from=None, date_to=None):
        return InventoryRepository.list_checks(
            status=status,
            search=search,
            date_from=date_from,
            date_to=date_to,
        )

    @staticmethod
    def create_check(audit_date, note, product_ids, user):
        if not product_ids:
            raise ValidationError('Can it nhat 1 san pham de thuc hien kiem ke.')

        product_ids = list(dict.fromkeys(str(pid) for pid in product_ids))
        validated_products = list(
            Product.objects.filter(id__in=product_ids).values_list('id', flat=True)
        )
        if len(validated_products) != len(product_ids):
            raise ValidationError('Co san pham khong hop le hoac da bi xoa.')

        return InventoryRepository.create_check(
            audit_date=audit_date,
            note=note,
            product_ids=validated_products,
            user=user,
        )

    @staticmethod
    def get_check_detail(check_id):
        audit = InventoryRepository.get_by_id(check_id)
        if not audit:
            raise ValidationError('Khong tim thay phien kiem ke.')

        items = list(audit.items.select_related('product').all())
        total_discrepancy = sum((item.discrepancy for item in items), Decimal('0'))

        summary = {
            'total_products': len(items),
            'products_with_loss': sum(1 for item in items if item.discrepancy < 0),
            'products_with_surplus': sum(1 for item in items if item.discrepancy > 0),
            'total_discrepancy_qty': total_discrepancy,
        }
        return audit, items, summary

    @staticmethod
    def update_item_actual(check_id, item_id, actual_quantity, note=''):
        audit = InventoryRepository.get_by_id(check_id)
        if not audit:
            raise ValidationError('Khong tim thay phien kiem ke.')

        if audit.status != InventoryAudit.Status.DRAFT:
            raise ValidationError('Chi phien o trang thai DRAFT moi duoc cap nhat so thuc te.')

        item = InventoryRepository.update_item(
            audit=audit,
            item_id=item_id,
            actual_quantity=actual_quantity,
            note=note,
        )
        if not item:
            raise ValidationError('Khong tim thay dong kiem ke can cap nhat.')

        return item

    @staticmethod
    def submit_check(check_id):
        audit = InventoryRepository.get_by_id(check_id)
        if not audit:
            raise ValidationError('Khong tim thay phien kiem ke.')

        if audit.status != InventoryAudit.Status.DRAFT:
            raise ValidationError('Chi phien DRAFT moi duoc nop duyet.')

        return InventoryRepository.submit_check(audit)

    @staticmethod
    def approve_check(check_id, approved_by):
        audit = InventoryRepository.get_by_id(check_id)
        if not audit:
            raise ValidationError('Khong tim thay phien kiem ke.')

        if audit.status != InventoryAudit.Status.SUBMITTED:
            raise ValidationError(f'Khong the duyet phien o trang thai {audit.status}.')

        return InventoryRepository.approve_check(audit, approved_by)

    @staticmethod
    def cancel_check(check_id, reason=''):
        audit = InventoryRepository.get_by_id(check_id)
        if not audit:
            raise ValidationError('Khong tim thay phien kiem ke.')

        if audit.status == InventoryAudit.Status.APPROVED:
            raise ValidationError('Khong the huy phien da duoc duyet.')

        if audit.status == InventoryAudit.Status.CANCELLED:
            raise ValidationError('Phien da o trang thai huy.')

        return InventoryRepository.cancel_check(audit, reason)

    @staticmethod
    def get_check_discrepancy(check_id):
        audit = InventoryRepository.get_by_id(check_id)
        if not audit:
            raise ValidationError('Khong tim thay phien kiem ke.')

        discrepancies = InventoryRepository.get_discrepancy(check_id)
        result = []
        for item in discrepancies:
            diff = item['calculated_discrepancy']
            if diff < 0:
                status_flag = 'SHORTAGE'
            elif diff > 0:
                status_flag = 'SURPLUS'
            else:
                status_flag = 'MATCH'

            item['status_flag'] = status_flag
            result.append(item)

        return result


class LossService:
    """Service handling business rules for InventoryLoss workflows."""

    @staticmethod
    def list_losses(loss_type=None, status=None, date_from=None, date_to=None, product_id=None, search=None):
        return LossRepository.list_losses(
            loss_type=loss_type,
            status=status,
            date_from=date_from,
            date_to=date_to,
            product_id=product_id,
            search=search,
        )

    @staticmethod
    def get_loss(loss_id):
        loss = LossRepository.get_by_id(loss_id)
        if not loss:
            raise ValidationError('Khong tim thay phieu hao hut.')
        return loss

    @staticmethod
    def create_loss(product_id, loss_quantity, loss_type, loss_reason, loss_date, user, audit_item_id=None, unit_cost=None):
        if Decimal(str(loss_quantity)) <= 0:
            raise ValidationError('So luong hao hut phai lon hon 0.')

        valid_types = [choice[0] for choice in InventoryLoss.LossType.choices]
        if loss_type not in valid_types:
            raise ValidationError(f'Loai hao hut khong hop le. Ho tro: {", ".join(valid_types)}.')

        if not loss_reason or len(loss_reason.strip()) < 5:
            raise ValidationError('Vui long mo ta ly do hao hut toi thieu 5 ky tu.')

        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise ValidationError('Khong tim thay san pham.')

        audit_item = None
        if audit_item_id:
            from .models import InventoryAuditItem

            audit_item = InventoryAuditItem.objects.filter(id=audit_item_id).first()
            if audit_item is None:
                raise ValidationError('Lien ket dong kiem ke khong hop le.')

        final_unit_cost = Decimal(str(unit_cost)) if unit_cost is not None else product.base_price

        return LossRepository.create_loss(
            product_id=product_id,
            loss_quantity=loss_quantity,
            loss_type=loss_type,
            loss_reason=loss_reason.strip(),
            loss_date=loss_date,
            unit_cost=final_unit_cost,
            user=user,
            audit_item=audit_item,
        )

    @staticmethod
    def update_loss(loss_id, loss_type=None, loss_reason=None):
        loss = LossRepository.get_by_id(loss_id)
        if not loss:
            raise ValidationError('Khong tim thay phieu hao hut.')

        if loss.status != InventoryLoss.Status.PENDING:
            raise ValidationError('Chi phieu hao hut PENDING moi duoc cap nhat.')

        if loss_type is not None:
            valid_types = [choice[0] for choice in InventoryLoss.LossType.choices]
            if loss_type not in valid_types:
                raise ValidationError('Loai hao hut khong hop le.')

        if loss_reason is not None and len(loss_reason.strip()) < 5:
            raise ValidationError('Ly do hao hut phai co it nhat 5 ky tu.')

        return LossRepository.update_loss(loss, loss_type=loss_type, loss_reason=loss_reason.strip() if loss_reason else loss_reason)

    @staticmethod
    def approve_loss(loss_id, reviewed_by):
        loss = LossRepository.get_by_id(loss_id)
        if not loss:
            raise ValidationError('Khong tim thay phieu hao hut.')

        if loss.status != InventoryLoss.Status.PENDING:
            raise ValidationError('Chi phieu hao hut PENDING moi duoc duyet.')

        return LossRepository.approve_loss(loss, reviewed_by)

    @staticmethod
    def reject_loss(loss_id, reviewed_by, rejection_note):
        loss = LossRepository.get_by_id(loss_id)
        if not loss:
            raise ValidationError('Khong tim thay phieu hao hut.')

        if loss.status != InventoryLoss.Status.PENDING:
            raise ValidationError('Chi phieu hao hut PENDING moi duoc tu choi.')

        if not rejection_note or len(rejection_note.strip()) < 3:
            raise ValidationError('Vui long ghi ly do tu choi.')

        return LossRepository.reject_loss(loss, reviewed_by, rejection_note.strip())

    @staticmethod
    def get_stats(date_from=None, date_to=None, loss_type=None, product_id=None):
        by_type = list(
            LossRepository.aggregate_by_type(
                date_from=date_from,
                date_to=date_to,
                loss_type=loss_type,
                product_id=product_id,
            )
        )
        by_month = list(
            LossRepository.aggregate_by_month(
                date_from=date_from,
                date_to=date_to,
                loss_type=loss_type,
                product_id=product_id,
            )
        )
        top_products = list(
            LossRepository.top_products(
                date_from=date_from,
                date_to=date_to,
                loss_type=loss_type,
                product_id=product_id,
            )
        )

        type_labels = dict(InventoryLoss.LossType.choices)

        return {
            'by_type': [
                {
                    'loss_type': row['loss_type'],
                    'label': type_labels.get(row['loss_type'], row['loss_type']),
                    'count': row['count'],
                    'total_quantity': row['total_quantity'],
                    'total_value': row['total_value'],
                }
                for row in by_type
            ],
            'by_month': [
                {
                    'month': row['month'].strftime('%Y-%m') if row['month'] else '',
                    'total_quantity': row['total_quantity'],
                    'total_value': row['total_value'],
                }
                for row in by_month
            ],
            'top_products': [
                {
                    'product_id': row['product_id'],
                    'product_name': row['product__name'],
                    'total_quantity': row['total_quantity'],
                    'total_value': row['total_value'],
                }
                for row in top_products
            ],
        }



