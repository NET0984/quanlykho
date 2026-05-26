from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View

from apps.product.models import Category, Product

from .models import InventoryAudit, InventoryLoss
from apps.reports.generators import AuditReportGenerator, DiscrepancyReportGenerator, LossReportGenerator
from apps.reports.repositories import ReportRepository
from apps.reports.services import LossReportService
from .services import InventoryService, LossService

PAGE_SIZE = 10


def _role(user):
    if getattr(user, 'is_superuser', False):
        return 'ADMIN'
    return getattr(user, 'role', '')


def _user_display_name(user):
    full_name = (getattr(user, 'full_name', '') or '').strip()
    return full_name or getattr(user, 'username', '') or 'Unknown'


def _parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


def _query_value(query_dict, key):
    return (query_dict.get(key) or '').strip()


def _export_filters(payload):
    result = {}
    for key, value in payload.items():
        if value not in (None, ''):
            result[key] = str(value)
    return result


def _is_allowed(user, allowed_roles):
    return _role(user) in allowed_roles


class InventoryAuditListView(LoginRequiredMixin, View):
    def _deny(self, request):
        messages.error(request, 'Bạn không có quyền truy cập màn hình kiểm kê.')
        return redirect('dashboard')

    def get(self, request):
        user_role = _role(request.user)
        if not _is_allowed(request.user, ('KHO', 'KE_TOAN', 'ADMIN')):
            return self._deny(request)

        status_filter = _query_value(request.GET, 'status')
        search_query = _query_value(request.GET, 'search')
        date_from_raw = _query_value(request.GET, 'date_from')
        date_to_raw = _query_value(request.GET, 'date_to')

        date_from = _parse_date(date_from_raw)
        date_to = _parse_date(date_to_raw)
        if date_from_raw and date_from is None:
            messages.error(request, 'Ngày bắt đầu không hợp lệ. Đã bỏ qua bộ lọc này.')
        if date_to_raw and date_to is None:
            messages.error(request, 'Ngày kết thúc không hợp lệ. Đã bỏ qua bộ lọc này.')

        if date_from and date_to and date_from > date_to:
            messages.error(request, 'Ngày bắt đầu không được lớn hơn ngày kết thúc.')
            date_from = None
            date_to = None

        audits = InventoryService.list_checks(
            status=status_filter or None,
            search=search_query or None,
            date_from=date_from,
            date_to=date_to,
        )

        paginator = Paginator(audits, PAGE_SIZE)
        page_obj = paginator.get_page(request.GET.get('page', 1))

        all_audits = InventoryService.list_checks()
        context = {
            'audits': page_obj,
            'page_obj': page_obj,
            'paginator': paginator,
            'statuses': InventoryAudit.Status.choices,
            'status_filter': status_filter,
            'search_query': search_query,
            'date_from': date_from_raw,
            'date_to': date_to_raw,
            'user_role': user_role,
            'stats': {
                'total': all_audits.count(),
                'draft': all_audits.filter(status=InventoryAudit.Status.DRAFT).count(),
                'submitted': all_audits.filter(status=InventoryAudit.Status.SUBMITTED).count(),
                'approved': all_audits.filter(status=InventoryAudit.Status.APPROVED).count(),
            },
        }
        return render(request, 'inventory/audit_list.html', context)


class InventoryAuditCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if not _is_allowed(request.user, ('KHO', 'ADMIN')):
            messages.error(request, 'Bạn không có quyền tạo phiên kiểm kê.')
            return redirect('inventory:audit_list')
        
        context = {
            'products': Product.objects.select_related('category').all().order_by('name'),
            'default_audit_date': timezone.localdate().isoformat(),
            'user_role': _role(request.user),
        }
        return render(request, 'inventory/audit_create.html', context)

    def post(self, request):
        if not _is_allowed(request.user, ('KHO', 'ADMIN')):
            messages.error(request, 'Bạn không có quyền tạo phiên kiểm kê.')
            return redirect('inventory:audit_list')

        audit_date = _parse_date(_query_value(request.POST, 'audit_date'))
        note = _query_value(request.POST, 'note')
        product_ids = request.POST.getlist('product_ids')

        if audit_date is None:
            messages.error(request, 'Vui lòng nhập ngày kiểm kê hợp lệ.')
            return render(request, 'inventory/audit_create.html', {
                'products': Product.objects.select_related('category').all().order_by('name'),
                'default_audit_date': timezone.localdate().isoformat(),
                'user_role': _role(request.user),
            })

        if not product_ids:
            messages.error(request, 'Vui lòng chọn ít nhất 1 sản phẩm để kiểm kê.')
            return render(request, 'inventory/audit_create.html', {
                'products': Product.objects.select_related('category').all().order_by('name'),
                'default_audit_date': timezone.localdate().isoformat(),
                'user_role': _role(request.user),
            })

        try:
            audit = InventoryService.create_check(
                audit_date=audit_date,
                note=note,
                product_ids=product_ids,
                user=request.user,
            )
        except DjangoValidationError as exc:
            messages.error(request, str(exc.message))
            return render(request, 'inventory/audit_create.html', {
                'products': Product.objects.select_related('category').all().order_by('name'),
                'default_audit_date': timezone.localdate().isoformat(),
                'user_role': _role(request.user),
            })

        messages.success(request, f'Da tao phien kiem ke {audit.audit_code}.')
        return redirect('inventory:audit_detail', audit_id=audit.id)


class InventoryAuditDetailView(LoginRequiredMixin, View):
    def _deny(self, request):
        messages.error(request, 'Bạn không có quyền truy cập chi tiết kiểm kê.')
        return redirect('inventory:audit_list')

    def get(self, request, audit_id):
        user_role = _role(request.user)
        if not _is_allowed(request.user, ('KHO', 'KE_TOAN', 'ADMIN')):
            return self._deny(request)

        try:
            audit, items, summary = InventoryService.get_check_detail(audit_id)
        except DjangoValidationError as exc:
            messages.error(request, str(exc.message))
            return redirect('inventory:audit_list')

        context = {
            'audit': audit,
            'items': items,
            'summary': summary,
            'user_role': user_role,
            'can_edit_items': audit.status == InventoryAudit.Status.DRAFT and user_role in ('KHO', 'ADMIN'),
            'can_submit': audit.status == InventoryAudit.Status.DRAFT and user_role in ('KHO', 'ADMIN'),
            'can_approve': audit.status == InventoryAudit.Status.SUBMITTED and user_role in ('KE_TOAN', 'ADMIN'),
            'can_cancel': audit.status not in (InventoryAudit.Status.APPROVED, InventoryAudit.Status.CANCELLED) and user_role == 'ADMIN',
            'can_export': user_role in ('KE_TOAN', 'ADMIN'),
        }
        return render(request, 'inventory/audit_detail.html', context)

    def post(self, request, audit_id):
        action = _query_value(request.POST, 'action')
        user_role = _role(request.user)

        if action == 'save_all_items':
            if user_role not in ('KHO', 'ADMIN'):
                return self._deny(request)
            
            item_ids = request.POST.getlist('item_id')
            has_error = False
            for item_id in item_ids:
                actual_quantity = _query_value(request.POST, f'actual_quantity_{item_id}')
                note = _query_value(request.POST, f'note_{item_id}')
                
                if actual_quantity:
                    try:
                        InventoryService.update_item_actual(
                            check_id=audit_id,
                            item_id=item_id,
                            actual_quantity=actual_quantity,
                            note=note,
                        )
                    except DjangoValidationError as exc:
                        messages.error(request, f'Lỗi khi lưu sản phẩm có ID {item_id}: {exc.message}')
                        has_error = True
                        
            if not has_error:
                messages.success(request, 'Đã lưu tất cả sản phẩm kiểm kê.')
            return redirect('inventory:audit_detail', audit_id=audit_id)

        if action == 'submit':
            if user_role not in ('KHO', 'ADMIN'):
                return self._deny(request)
            try:
                InventoryService.submit_check(audit_id)
                messages.success(request, 'Đã nộp phiên kiểm kê cho kế toán duyệt.')
            except DjangoValidationError as exc:
                messages.error(request, str(exc.message))
            return redirect('inventory:audit_detail', audit_id=audit_id)

        if action == 'approve':
            if user_role not in ('KE_TOAN', 'ADMIN'):
                return self._deny(request)
            try:
                InventoryService.approve_check(audit_id, request.user)
                messages.success(request, 'Đã duyệt phiên kiểm kê và cập nhật tồn kho.')
            except DjangoValidationError as exc:
                messages.error(request, str(exc.message))
            return redirect('inventory:audit_detail', audit_id=audit_id)

        if action == 'cancel':
            if user_role != 'ADMIN':
                return self._deny(request)
            reason = _query_value(request.POST, 'reason')
            try:
                InventoryService.cancel_check(audit_id, reason)
                messages.warning(request, 'Đã hủy phiên kiểm kê.')
            except DjangoValidationError as exc:
                messages.error(request, str(exc.message))
            return redirect('inventory:audit_detail', audit_id=audit_id)

        messages.error(request, 'Thao tác không hợp lệ.')
        return redirect('inventory:audit_detail', audit_id=audit_id)


class InventoryAuditExportView(LoginRequiredMixin, View):
    def get(self, request, audit_id):
        if not _is_allowed(request.user, ('KE_TOAN', 'ADMIN')):
            messages.error(request, 'Bạn không có quyền xuất báo cáo kiểm kê.')
            return redirect('inventory:audit_detail', audit_id=audit_id)

        export_format = _query_value(request.GET, 'format') or 'excel'
        audit, rows = ReportRepository.audit_report_rows(audit_id)
        if audit is None:
            messages.error(request, 'Không tìm thấy phiên kiểm kê.')
            return redirect('inventory:audit_list')

        try:
            filters = _export_filters({'audit_id': audit_id})
            generator = AuditReportGenerator(audit=audit, data=rows, filters=filters)
            response = generator.as_http_response(export_format)
            ReportRepository.log_export(
                report_type='AUDIT_REPORT',
                export_format=export_format.upper(),
                exported_by=request.user,
                filter_params=filters,
                row_count=len(rows),
            )
            return response
        except ValueError:
            messages.error(request, 'Định dạng xuất không được hỗ trợ.')
            return redirect('inventory:audit_detail', audit_id=audit_id)


class InventoryLossListView(LoginRequiredMixin, View):
    def _deny(self, request):
        messages.error(request, 'Bạn không có quyền truy cập màn hình hao hụt.')
        return redirect('dashboard')

    def get(self, request):
        user_role = _role(request.user)
        if not _is_allowed(request.user, ('KHO', 'KE_TOAN', 'ADMIN')):
            return self._deny(request)

        status_filter = _query_value(request.GET, 'status')
        type_filter = _query_value(request.GET, 'loss_type')
        search_query = _query_value(request.GET, 'search')
        product_id = _query_value(request.GET, 'product_id')
        date_from_raw = _query_value(request.GET, 'date_from')
        date_to_raw = _query_value(request.GET, 'date_to')

        date_from = _parse_date(date_from_raw)
        date_to = _parse_date(date_to_raw)
        if date_from_raw and date_from is None:
            messages.error(request, 'Ngày bắt đầu không hợp lệ. Đã bỏ qua bộ lọc này.')
        if date_to_raw and date_to is None:
            messages.error(request, 'Ngày kết thúc không hợp lệ. Đã bỏ qua bộ lọc này.')
        if date_from and date_to and date_from > date_to:
            messages.error(request, 'Ngày bắt đầu không được lớn hơn ngày kết thúc.')
            date_from = None
            date_to = None

        losses = LossService.list_losses(
            loss_type=type_filter or None,
            status=status_filter or None,
            date_from=date_from,
            date_to=date_to,
            product_id=product_id or None,
            search=search_query or None,
        )

        paginator = Paginator(losses, PAGE_SIZE)
        page_obj = paginator.get_page(request.GET.get('page', 1))

        stats_payload = LossService.get_stats(
            date_from=date_from,
            date_to=date_to,
            loss_type=type_filter or None,
            product_id=product_id or None,
        )
        total_quantity = sum((row['total_quantity'] for row in stats_payload['by_type']), Decimal('0'))
        total_value = sum((row['total_value'] for row in stats_payload['by_type']), Decimal('0'))

        context = {
            'losses': page_obj,
            'page_obj': page_obj,
            'paginator': paginator,
            'statuses': InventoryLoss.Status.choices,
            'loss_types': InventoryLoss.LossType.choices,
            'status_filter': status_filter,
            'type_filter': type_filter,
            'search_query': search_query,
            'product_id': product_id,
            'date_from': date_from_raw,
            'date_to': date_to_raw,
            'products': Product.objects.select_related('category').all().order_by('name'),
            'default_loss_date': timezone.localdate().isoformat(),
            'user_role': user_role,
            'stats': {
                'total_records': paginator.count,
                'pending_records': losses.filter(status=InventoryLoss.Status.PENDING).count(),
                'total_quantity': total_quantity,
                'total_value': total_value,
            },
        }
        return render(request, 'inventory/loss_list.html', context)

    def post(self, request):
        user_role = _role(request.user)
        action = _query_value(request.POST, 'action')

        if action == 'create':
            if user_role not in ('KHO', 'ADMIN'):
                return self._deny(request)

            product_id = _query_value(request.POST, 'product_id')
            loss_quantity = _query_value(request.POST, 'loss_quantity')
            loss_type = _query_value(request.POST, 'loss_type')
            loss_reason = _query_value(request.POST, 'loss_reason')
            loss_date = _parse_date(_query_value(request.POST, 'loss_date'))
            unit_cost = _query_value(request.POST, 'unit_cost')
            unit_cost = unit_cost if unit_cost else None

            if loss_date is None:
                messages.error(request, 'Vui long nhap ngay hao hut hop le.')
                return redirect('inventory:loss_list')

            try:
                loss = LossService.create_loss(
                    product_id=product_id,
                    loss_quantity=loss_quantity,
                    loss_type=loss_type,
                    loss_reason=loss_reason,
                    loss_date=loss_date,
                    unit_cost=unit_cost,
                    user=request.user,
                )
                messages.success(request, f'Đã tạo phiếu hao hụt {loss.loss_code}.')
            except DjangoValidationError as exc:
                messages.error(request, str(exc.message))
            return redirect('inventory:loss_list')

        if action == 'update':
            if user_role not in ('KHO', 'ADMIN'):
                return self._deny(request)

            loss_id = _query_value(request.POST, 'loss_id')
            loss_type = _query_value(request.POST, 'loss_type')
            loss_reason = _query_value(request.POST, 'loss_reason')
            try:
                LossService.update_loss(loss_id=loss_id, loss_type=loss_type, loss_reason=loss_reason)
                messages.success(request, 'Đã cập nhật phiếu hao hụt.')
            except DjangoValidationError as exc:
                messages.error(request, str(exc.message))
            return redirect('inventory:loss_list')

        if action == 'approve':
            if user_role not in ('KE_TOAN', 'ADMIN'):
                return self._deny(request)

            loss_id = _query_value(request.POST, 'loss_id')
            try:
                LossService.approve_loss(loss_id=loss_id, reviewed_by=request.user)
                messages.success(request, 'Đã duyệt phiếu hao hụt.')
            except DjangoValidationError as exc:
                messages.error(request, str(exc.message))
            return redirect('inventory:loss_list')

        if action == 'reject':
            if user_role not in ('KE_TOAN', 'ADMIN'):
                return self._deny(request)

            loss_id = _query_value(request.POST, 'loss_id')
            rejection_note = _query_value(request.POST, 'rejection_note')
            try:
                LossService.reject_loss(loss_id=loss_id, reviewed_by=request.user, rejection_note=rejection_note)
                messages.warning(request, 'Đã từ chối phiếu hao hụt.')
            except DjangoValidationError as exc:
                messages.error(request, str(exc.message))
            return redirect('inventory:loss_list')

        messages.error(request, 'Thao tác không hợp lệ.')
        return redirect('inventory:loss_list')


class InventoryLossExportView(LoginRequiredMixin, View):
    def get(self, request):
        if not _is_allowed(request.user, ('KE_TOAN', 'ADMIN')):
            messages.error(request, 'Bạn không có quyền xuất báo cáo hao hụt.')
            return redirect('inventory:loss_list')

        export_format = _query_value(request.GET, 'format') or 'excel'
        date_from = _parse_date(_query_value(request.GET, 'date_from'))
        date_to = _parse_date(_query_value(request.GET, 'date_to'))
        loss_type = _query_value(request.GET, 'loss_type') or None

        if date_from and date_to and date_from > date_to:
            messages.error(request, 'Ngày bắt đầu không được lớn hơn ngày kết thúc.')
            return redirect('inventory:loss_list')

        rows = list(
            ReportRepository.loss_report_rows(
                date_from=date_from,
                date_to=date_to,
                loss_type=loss_type,
            )
        )

        filters = _export_filters(
            {
                'date_from': date_from,
                'date_to': date_to,
                'loss_type': loss_type,
            }
        )

        try:
            generator = LossReportGenerator(rows, filters=filters)
            response = generator.as_http_response(export_format)
            ReportRepository.log_export(
                report_type='LOSS_REPORT',
                export_format=export_format.upper(),
                exported_by=request.user,
                filter_params=filters,
                row_count=len(rows),
            )
            return response
        except ValueError:
            messages.error(request, 'Định dạng xuất không được hỗ trợ.')
            return redirect('inventory:loss_list')


class InventoryDiscrepancyView(LoginRequiredMixin, View):
    def _deny(self, request):
        messages.error(request, 'Bạn không có quyền truy cập báo cáo chênh lệch.')
        return redirect('dashboard')

    def get(self, request):
        user_role = _role(request.user)
        if not _is_allowed(request.user, ('KHO', 'KE_TOAN', 'ADMIN')):
            return self._deny(request)

        product_id = _query_value(request.GET, 'product_id') or None
        category_id = _query_value(request.GET, 'category_id') or None

        report_data = LossReportService.generate_discrepancy_report(
            product_id=product_id,
            category_id=category_id,
        )

        context = {
            'items': report_data['items'],
            'summary': report_data['summary'],
            'generated_at': report_data['generated_at'],
            'product_id': product_id or '',
            'category_id': category_id or '',
            'products': Product.objects.select_related('category').all().order_by('name'),
            'categories': Category.objects.all().order_by('name'),
            'user_role': user_role,
            'can_export': user_role in ('KE_TOAN', 'ADMIN'),
        }
        return render(request, 'inventory/discrepancy_report.html', context)


class InventoryDiscrepancyExportView(LoginRequiredMixin, View):
    def get(self, request):
        if not _is_allowed(request.user, ('KE_TOAN', 'ADMIN')):
            messages.error(request, 'Bạn không có quyền xuất báo cáo chênh lệch.')
            return redirect('inventory:discrepancy_report')

        export_format = _query_value(request.GET, 'format') or 'excel'
        product_id = _query_value(request.GET, 'product_id') or None
        category_id = _query_value(request.GET, 'category_id') or None

        rows = list(ReportRepository.discrepancy_rows(product_id=product_id, category_id=category_id))
        filters = _export_filters({'product_id': product_id, 'category_id': category_id})

        try:
            generator = DiscrepancyReportGenerator(rows, filters=filters)
            response = generator.as_http_response(export_format)
            ReportRepository.log_export(
                report_type='DISCREPANCY',
                export_format=export_format.upper(),
                exported_by=request.user,
                filter_params=filters,
                row_count=len(rows),
            )
            return response
        except ValueError:
            messages.error(request, 'Định dạng xuất không được hỗ trợ.')
            return redirect(f"{reverse('inventory:discrepancy_report')}")
