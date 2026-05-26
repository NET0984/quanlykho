from django.contrib import admin
from .models import ReportExportLog

@admin.register(ReportExportLog)
class ReportExportLogAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'export_format', 'exported_by', 'exported_at', 'row_count')
    list_filter = ('report_type', 'export_format', 'exported_at')
    search_fields = ('exported_by__username', 'exported_by__email')
    readonly_fields = ('exported_at',)
