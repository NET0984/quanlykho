from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # 1. Các cột hiển thị ở danh sách tài khoản
    list_display = ('username', 'full_name', 'email', 'role', 'is_staff', 'is_active')
    
    # 2. Bộ lọc bên phải (Rất hữu ích để lọc nhân viên theo vai trò)
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    
    # 3. Các trường cho phép tìm kiếm nhanh
    search_fields = ('username', 'full_name', 'email', 'phone_number')
    
    # 4. Sắp xếp danh sách theo tên đăng nhập
    ordering = ('username',)

    # 5. CẤU HÌNH TRANG CHỈNH SỬA (Fieldsets)
    # Thêm nhóm "Thông tin hệ thống uclickvn" vào giao diện admin
    fieldsets = UserAdmin.fieldsets + (
        ('Thông tin uclickvn', {
            'fields': ('full_name', 'role', 'phone_number', 'address'),
        }),
    )

    # 6. CẤU HÌNH TRANG THÊM MỚI (Add Fieldsets)
    # Đảm bảo các trường mới cũng xuất hiện khi bạn tạo User trực tiếp từ Admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Thông tin bổ sung', {
            'classes': ('wide',),
            'fields': ('full_name', 'role', 'email'),
        }),
    )

# Đăng ký model với class CustomUserAdmin
admin.site.register(User, CustomUserAdmin)