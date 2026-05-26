from django.contrib import admin
from .models import ImportReceipt, ImportReceiptItem, ProductStock

# Hiển thị các dòng sản phẩm ngay bên trong phiếu nhập kho
class ImportReceiptItemInline(admin.TabularInline):
    model = ImportReceiptItem
    extra = 1

@admin.register(ImportReceipt)
class ImportReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_code', 'status', 'created_by', 'created_at', 'total_items')
    list_filter = ('status', 'created_at')
    search_fields = ('receipt_code',)
    inlines = [ImportReceiptItemInline]
    # Phân nhóm thông tin trong trang chi tiết
    fieldsets = (
        ('Thông tin cơ bản', {'fields': ('receipt_code', 'status', 'created_by')}),
        ('Ghi chú', {'fields': ('note', 'rejection_note')}),
        ('Duyệt phiếu', {'fields': ('reviewed_by', 'reviewed_at')}),
    )

@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'last_updated')
    search_fields = ('product__name',) # Tìm kiếm theo tên sản phẩm