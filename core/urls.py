"""
URL configuration for the project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', views.health_check, name='health_check'),

    # Auth pages
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Main page
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('accounts/', views.accounts_view, name='accounts'),
    path('account/settings/', views.profile_settings_view, name='profile_settings'),

    # App routes
    path('', include('apps.product.urls')),
    path('', include('apps.order.urls')),
    path('', include('apps.warehouse.urls')),
    path('', include('apps.inventory.urls')),

    # Authentication API
    path('api/xac-thuc/', include('apps.authentication.urls')),
    path('api/reports/', include('apps.reports.api_urls')),
    path('reports/', include('apps.reports.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
