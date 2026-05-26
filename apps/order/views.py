import json
from datetime import datetime, timedelta
from decimal import Decimal

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.utils import timezone

from apps.product.models import Product

from .models import SalesOrder, SalesOrderItem
from .services import SalesOrderService


PAGE_SIZE = 5


def _products_json():
    products = Product.objects.select_related('category').all().order_by('name')
    return [
        {
            'id': str(product.id),
            'name': product.name,
            'base_unit': product.base_unit,
            'base_price': float(product.base_price),
            'category': product.category.name if product.category else '',
        }
        for product in products
    ]


def _stocks_json():
    from apps.warehouse.repositories import ProductStockRepository

    stocks = ProductStockRepository.get_all()
    return {str(s.product_id): float(s.available_quantity) for s in stocks}


def _parse_items_from_post(post_data):
    items = []
    index = 0
    while True:
        product_id = post_data.get(f'product_id_{index}')
        if product_id is None:
            break
        if product_id:
            items.append(
                {
                    'product_id': product_id,
                    'quantity': post_data.get(f'quantity_{index}', 0),
                    'unit_price': post_data.get(f'unit_price_{index}', 0),
                    'note': post_data.get(f'item_note_{index}', ''),
                }
            )
        index += 1
    return items


def _get_sales_order_stats():
    today = timezone.now().date()
    return {
        'total_orders': SalesOrder.objects.count(),
        'pending_orders': SalesOrder.objects.filter(status='WAITING').count(),
        'picked_orders': SalesOrder.objects.filter(status='PICKED').count(),
        'total_items': SalesOrderItem.objects.aggregate(total=Sum('quantity'))['total'] or 0,
        'today_transactions': SalesOrder.objects.filter(created_at__date=today).count(),
    }


def _get_user_display_name(user):
    full_name = ''
    if hasattr(user, 'get_full_name'):
        full_name = (user.get_full_name() or '').strip()
    return full_name or getattr(user, 'username', '') or 'Khong ro'


def _parse_sales_report_filters(request):
    today = timezone.localdate()
    default_from = today - timedelta(days=365)

    status_filter = request.GET.get('status', '').strip()
    search_query = request.GET.get('search', '').strip()
    from_date_str = request.GET.get('from_date', default_from.isoformat())
    to_date_str = request.GET.get('to_date', today.isoformat())

    try:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
    except ValueError:
        from_date = default_from
        to_date = today
        messages.error(request, 'Khoảng thời gian không hợp lệ. Hệ thống đã dùng mặc định tháng hiện tại.')

    is_valid_range = True
    if from_date > to_date:
        is_valid_range = False
        messages.error(request, 'Ngày bắt đầu không được lớn hơn ngày kết thúc. Vui lòng chọn lại khoảng thời gian.')

    return status_filter, search_query, from_date, to_date, is_valid_range


def _get_base_orders_for_user(service, user):
    if user.role in ('KE_TOAN', 'ADMIN'):
        return service.get_all()
    if user.role == 'SALE':
        return service.get_by_user(user)
    return service.get_all()


def _apply_sales_order_filters(orders, status_filter, search_query, from_date, to_date):
    if status_filter:
        orders = orders.filter(status=status_filter)

    if search_query:
        orders = orders.filter(
            Q(customer_name__icontains=search_query) |
            Q(order_code__icontains=search_query)
        )

    return orders.filter(
        created_at__date__gte=from_date,
        created_at__date__lte=to_date,
    )


def _format_report_number(value):
    decimal_value = Decimal(str(value))
    formatted = f"{decimal_value:,.10f}".rstrip('0').rstrip('.')
    return formatted or '0'


class SalesOrderListView(LoginRequiredMixin, View):
    def get(self, request):
        service = SalesOrderService()
        user = request.user
        status_filter, search_query, from_date, to_date, is_valid_range = _parse_sales_report_filters(request)
        page_number = request.GET.get('page', 1)

        orders = _get_base_orders_for_user(service, user)
        if is_valid_range:
            orders = _apply_sales_order_filters(orders, status_filter, search_query, from_date, to_date)
        else:
            orders = orders.none()

        paginator = Paginator(orders, PAGE_SIZE)
        page_obj = paginator.get_page(page_number)

        products_data = _products_json()
        stocks_data = _stocks_json()
        stats = _get_sales_order_stats()

        valid_transitions = SalesOrderService.VALID_TRANSITIONS
        user_role = 'ADMIN' if user.is_superuser else user.role

        return render(request, 'order/sales_order_list.html', {
            'orders': page_obj,
            'page_obj': page_obj,
            'paginator': paginator,
            'products_json': json.dumps(products_data, ensure_ascii=False),
            'stocks_json': json.dumps(stocks_data),
            'user_role': user_role,
            'status_filter': status_filter,
            'search_query': search_query,
            'from_date': from_date.isoformat(),
            'to_date': to_date.isoformat(),
            'stats': stats,
            'valid_transitions_json': json.dumps(valid_transitions),
        })

    def post(self, request):
        user = request.user
        action = request.POST.get('action', '')

        if action == 'update_status':
            if user.role == 'SALE' and not user.is_superuser:
                messages.error(request, 'Ban khong co quyen cap nhat trang thai don hang.')
                return redirect('order:sales_list')

            order_id = request.POST.get('order_id')
            new_status = request.POST.get('status')

            if new_status not in ['CONFIRMED', 'WAITING', 'PICKED', 'DONE', 'CANCELLED']:
                messages.error(request, 'Trang thai khong hop le.')
                return redirect('order:sales_list')

            success, message = SalesOrderService().update_status(order_id, new_status, updated_by=user)
            if success:
                if new_status == 'WAITING':
                    messages.success(
                        request,
                        f'{message} Phieu xuat kho da duoc tao va dang cho thu kho lay hang.',
                    )
                else:
                    messages.success(request, message)
            else:
                messages.error(request, message)
            return redirect('order:sales_list')

        if user.role not in ('SALE', 'ADMIN') and not user.is_superuser:
            messages.error(request, 'Ban khong co quyen tao don hang.')
            return redirect('order:sales_list')

        order, errors = SalesOrderService().create_order(
            request.POST.get('customer_name', ''),
            request.POST.get('customer_phone', ''),
            request.POST.get('note', ''),
            _parse_items_from_post(request.POST),
            user,
        )

        if order:
            messages.success(
                request,
                f'Don hang {order.order_code} da duoc tao. Chuyen sang trang thai cho lay hang de tao phieu xuat.',
            )
        else:
            for error in errors:
                messages.error(request, error['message'])
        return redirect('order:sales_list')




class SalesOrderDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = SalesOrderService().get_by_id(pk)
        if not order:
            messages.error(request, 'Khong tim thay don hang.')
            return redirect('order:sales_list')

        return render(request, 'order/sales_order_detail.html', {
            'order': order,
            'user_role': 'ADMIN' if request.user.is_superuser else request.user.role,
            'valid_transitions': SalesOrderService.VALID_TRANSITIONS.get(order.status, []),
        })

class SalesReportView(LoginRequiredMixin, View):
 
    def get(self, request):
        from django.db.models import (
            F, Sum, Count, ExpressionWrapper, DecimalField
        )
        from django.db.models.functions import TruncMonth, TruncDate
        from apps.order.models import SalesOrderItem
        from datetime import timedelta
        import json
 
        user = request.user
        service = SalesOrderService()
 
        # Phân quyền
        user_role = 'ADMIN' if user.is_superuser else user.role
        if user_role == 'SALE':
            base_qs = service.get_by_user(user)
        else:
            base_qs = service.get_all()
 
        # Bộ lọc ngày (mặc định 12 tháng gần nhất)
        today = timezone.localdate()
        default_from = (today.replace(day=1)).replace(
            year=today.year - 1 if today.month == 1 else today.year,
            month=12 if today.month == 1 else today.month,
        )
        # Đơn giản hơn: lùi 365 ngày
        default_from = today - timedelta(days=364)
        default_from = default_from.replace(day=1)
 
        from_date_str = request.GET.get('from_date', default_from.isoformat())
        to_date_str   = request.GET.get('to_date',   today.isoformat())
 
        try:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
            to_date   = datetime.strptime(to_date_str,   '%Y-%m-%d').date()
        except ValueError:
            from_date = default_from
            to_date   = today
 
        if from_date > to_date:
            from_date, to_date = default_from, today
 
        filtered_qs = base_qs.filter(
            created_at__date__gte=from_date,
            created_at__date__lte=to_date,
        )
 
        # ── Doanh thu & số đơn theo tháng ────────────────────
        monthly_counts = (
            filtered_qs
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(order_count=Count('id'))
            .order_by('month')
        )
        count_map = {
            r['month'].strftime('%Y-%m'): r['order_count']
            for r in monthly_counts
        }
 
        revenue_expr = ExpressionWrapper(
            F('quantity') * F('unit_price'),
            output_field=DecimalField(max_digits=20, decimal_places=4)
        )
        monthly_revenue = (
            SalesOrderItem.objects
            .filter(order__in=filtered_qs)
            .annotate(month=TruncMonth('order__created_at'))
            .values('month')
            .annotate(revenue=Sum(revenue_expr))
            .order_by('month')
        )
        revenue_map = {
            r['month'].strftime('%Y-%m'): float(r['revenue'] or 0)
            for r in monthly_revenue
        }
 
        # Tạo dãy tháng liên tiếp
        chart_labels  = []
        chart_revenue = []
        chart_orders  = []
        cur = from_date.replace(day=1)
        end_month = to_date.replace(day=1)
        while cur <= end_month:
            key = cur.strftime('%Y-%m')
            chart_labels.append(cur.strftime('%m/%Y'))
            chart_revenue.append(revenue_map.get(key, 0))
            chart_orders.append(count_map.get(key, 0))
            if cur.month == 12:
                cur = cur.replace(year=cur.year + 1, month=1)
            else:
                cur = cur.replace(month=cur.month + 1)
 
        # ── Thống kê trạng thái ───────────────────────────────
        status_stats = (
            filtered_qs.values('status').annotate(cnt=Count('id'))
        )
        status_map = {s['status']: s['cnt'] for s in status_stats}
 
        total_orders  = filtered_qs.count()
        total_revenue = sum(chart_revenue)
        done_orders   = status_map.get('DONE', 0)
        completion_rate = round(done_orders / total_orders * 100, 1) if total_orders else 0
 
        # ── Top sản phẩm bán chạy (chỉ đơn DONE) ─────────────
        top_products = (
            SalesOrderItem.objects
            .filter(order__in=filtered_qs, order__status='DONE')
            .values('product__name', 'product__base_unit')
            .annotate(
                total_qty=Sum('quantity'),
                total_rev=Sum(revenue_expr),
            )
            .order_by('-total_rev')[:10]
        )
 
        # ── Số đơn theo ngày (30 ngày gần nhất) ──────────────
        thirty_ago = to_date - timedelta(days=29)
        daily_raw = (
            filtered_qs
            .filter(created_at__date__gte=thirty_ago)
            .annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(cnt=Count('id'))
            .order_by('day')
        )
        daily_map = {r['day'].strftime('%Y-%m-%d'): r['cnt'] for r in daily_raw}
        daily_labels = []
        daily_counts = []
        d = thirty_ago
        while d <= to_date:
            daily_labels.append(d.strftime('%d/%m'))
            daily_counts.append(daily_map.get(d.strftime('%Y-%m-%d'), 0))
            d += timedelta(days=1)
 
        context = {
            'from_date': from_date.isoformat(),
            'to_date':   to_date.isoformat(),
            # Chart JSON
            'chart_labels_json':  json.dumps(chart_labels),
            'chart_revenue_json': json.dumps(chart_revenue),
            'chart_orders_json':  json.dumps(chart_orders),
            'daily_labels_json':  json.dumps(daily_labels),
            'daily_counts_json':  json.dumps(daily_counts),
            # Donut
            'status_confirmed': status_map.get('CONFIRMED', 0),
            'status_waiting':   status_map.get('WAITING', 0),
            'status_done':      status_map.get('DONE', 0),
            'status_cancelled': status_map.get('CANCELLED', 0),
            # KPIs
            'total_orders':     total_orders,
            'total_revenue':    total_revenue,
            'done_orders':      done_orders,
            'cancel_orders':    status_map.get('CANCELLED', 0),
            'pending_orders':   status_map.get('WAITING', 0) + status_map.get('CONFIRMED', 0),
            'completion_rate':  completion_rate,
            # Table
            'top_products':     top_products,
            'user_role':        user_role,
        }
        return render(request, 'order/sales_report.html', context)
