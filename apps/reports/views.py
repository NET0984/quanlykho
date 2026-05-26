from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from urllib.parse import urlencode
import uuid
from datetime import datetime

from apps.reports.utils import get_user_display_name
from apps.reports.services import StockReportService

def _resolve_report_category_label(service, category_id):
    label = 'Tat ca danh muc'
    if category_id:
        selected = next((cat for cat in service.get_categories() if str(cat.id) == category_id), None)
        if selected:
            label = selected.name
    return label

def _parse_stock_report_filters(request):
    today = timezone.localdate()
    first_day = today.replace(day=1)

    from_date_str = request.GET.get('from_date', first_day.isoformat())
    to_date_str = request.GET.get('to_date', today.isoformat())
    raw_category_id = request.GET.get('category', '').strip()

    category_id = ''
    if raw_category_id:
        try:
            uuid.UUID(raw_category_id)
            category_id = raw_category_id
        except ValueError:
            messages.error(request, 'Danh mục không hợp lệ. Hệ thống đã bỏ bộ lọc danh mục.')

    try:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
    except ValueError:
        from_date = first_day
        to_date = today
        messages.error(request, 'Khoảng thời gian không hợp lệ. Hệ thống đã dùng mặc định tháng hiện tại.')

    is_valid_range = True
    if from_date > to_date:
        is_valid_range = False
        messages.error(request, 'Ngày bắt đầu không được lớn hơn ngày kết thúc. Vui lòng chọn lại khoảng thời gian.')

    return from_date, to_date, category_id, is_valid_range

class StockReportView(LoginRequiredMixin, View):
    def get(self, request):
        service = StockReportService()
        from_date, to_date, category_id, is_valid_range = _parse_stock_report_filters(request)

        if is_valid_range:
            rows, totals = service.build_report(
                from_date=from_date,
                to_date=to_date,
                category_id=category_id or None,
            )
        else:
            rows = []
            totals = {
                'opening': 0,
                'import_qty': 0,
                'export_qty': 0,
                'closing': 0,
            }

        return render(request, 'warehouse/stock_report.html', {
            'rows': rows,
            'totals': totals,
            'categories': service.get_categories(),
            'from_date': from_date.isoformat(),
            'to_date': to_date.isoformat(),
            'category_id': category_id,
            'generated_at': timezone.localtime(),
            'generated_by': get_user_display_name(request.user),
            'user_role': 'ADMIN' if request.user.is_superuser else request.user.role,
        })

class StockReportExportExcelView(LoginRequiredMixin, View):
    def get(self, request):
        service = StockReportService()
        from_date, to_date, category_id, is_valid_range = _parse_stock_report_filters(request)

        if not is_valid_range:
            params = {
                'from_date': from_date.isoformat(),
                'to_date': to_date.isoformat(),
            }
            if category_id:
                params['category'] = category_id
            return redirect(f"{reverse('reports:stock_report')}?{urlencode(params)}")

        rows, totals = service.build_report(
            from_date=from_date,
            to_date=to_date,
            category_id=category_id or None,
        )
        
        category_label = _resolve_report_category_label(service, category_id)

        from apps.reports.exporters.stock import StockReportExporter
        return StockReportExporter.export_excel(
            rows, totals, from_date, to_date, category_label, get_user_display_name(request.user)
        )

class StockReportExportPdfView(LoginRequiredMixin, View):
    def get(self, request):
        service = StockReportService()
        from_date, to_date, category_id, is_valid_range = _parse_stock_report_filters(request)

        if not is_valid_range:
            params = {
                'from_date': from_date.isoformat(),
                'to_date': to_date.isoformat(),
            }
            if category_id:
                params['category'] = category_id
            return redirect(f"{reverse('reports:stock_report')}?{urlencode(params)}")

        rows, totals = service.build_report(
            from_date=from_date,
            to_date=to_date,
            category_id=category_id or None,
        )

        category_label = _resolve_report_category_label(service, category_id)

        from apps.reports.exporters.stock import StockReportExporter
        return StockReportExporter.export_pdf(
            rows, totals, from_date, to_date, category_label, get_user_display_name(request.user)
        )



from apps.order.services import SalesOrderService
from apps.order.views import _parse_sales_report_filters, _get_base_orders_for_user, _apply_sales_order_filters

class SalesOrderExportExcelView(LoginRequiredMixin, View):
    def get(self, request):
        service = SalesOrderService()
        status_filter, search_query, from_date, to_date, is_valid_range = _parse_sales_report_filters(request)

        if not is_valid_range:
            params = {
                'status': status_filter,
                'search': search_query,
                'from_date': from_date.isoformat(),
                'to_date': to_date.isoformat(),
            }
            params = {k: v for k, v in params.items() if v}
            return redirect(f"{reverse('order:sales_list')}?{urlencode(params)}")

        orders = _get_base_orders_for_user(service, request.user)
        orders = _apply_sales_order_filters(orders, status_filter, search_query, from_date, to_date)

        from apps.reports.exporters.sales import SalesOrderExporter
        return SalesOrderExporter.export_excel(
            orders, status_filter, search_query, from_date, to_date, get_user_display_name(request.user)
        )


class SalesOrderExportPdfView(LoginRequiredMixin, View):
    def get(self, request):
        service = SalesOrderService()
        status_filter, search_query, from_date, to_date, is_valid_range = _parse_sales_report_filters(request)

        if not is_valid_range:
            params = {
                'status': status_filter,
                'search': search_query,
                'from_date': from_date.isoformat(),
                'to_date': to_date.isoformat(),
            }
            params = {k: v for k, v in params.items() if v}
            return redirect(f"{reverse('order:sales_list')}?{urlencode(params)}")

        orders = _get_base_orders_for_user(service, request.user)
        orders = _apply_sales_order_filters(orders, status_filter, search_query, from_date, to_date)

        from apps.reports.exporters.sales import SalesOrderExporter
        return SalesOrderExporter.export_pdf(
            orders, status_filter, search_query, from_date, to_date, get_user_display_name(request.user)
        )

