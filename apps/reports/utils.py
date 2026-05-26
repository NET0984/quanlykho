from decimal import Decimal

def format_report_number(value):
    decimal_value = Decimal(str(value))
    formatted = f"{decimal_value:,.10f}".rstrip('0').rstrip('.')
    return formatted or '0'

def get_user_display_name(user):
    full_name = ''
    if hasattr(user, 'get_full_name'):
        full_name = (user.get_full_name() or '').strip()
    return full_name or getattr(user, 'username', '') or 'Khong ro'

from datetime import datetime
from django.utils import timezone

def parse_date_filters(request):
    today = timezone.localdate()
    first_day = today.replace(day=1)

    status_filter = request.GET.get('status', '').strip()
    search_query = request.GET.get('search', '').strip()
    from_date_str = request.GET.get('from_date', first_day.isoformat())
    to_date_str = request.GET.get('to_date', today.isoformat())

    try:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
    except ValueError:
        from_date = first_day
        to_date = today
        return status_filter, search_query, from_date, to_date, False, 'Khoảng thời gian không hợp lệ. Hệ thống đã dùng mặc định tháng hiện tại.'

    if from_date > to_date:
        return status_filter, search_query, from_date, to_date, False, 'Ngày bắt đầu không được lớn hơn ngày kết thúc. Vui lòng chọn lại khoảng thời gian.'

    return status_filter, search_query, from_date, to_date, True, None
