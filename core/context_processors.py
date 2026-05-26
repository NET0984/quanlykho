from core.views import _build_dashboard_notifications


def notifications_context(request):
    """Expose bell notifications for all pages using the shared base template."""
    if not request.user.is_authenticated:
        return {
            'notifications': [],
            'notifications_count': 0,
        }

    notifications = _build_dashboard_notifications(request.user)

    return {
        'notifications': notifications,
        'notifications_count': len(notifications),
    }
