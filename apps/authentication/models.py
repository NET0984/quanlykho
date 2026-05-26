from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator, MinLengthValidator
import uuid

# --- 1. NGƯỜI DÙNG (Custom User) ---
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        help_text="Tên đầy đủ, tối thiểu 2 ký tự"
    )
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{10,11}$',
                message='Số điện thoại phải có 10-11 chữ số',
                code='invalid_phone'
            )
        ]
    )
    address = models.TextField(null=True, blank=True)
    
    ROLE_CHOICES = [
        ('ADMIN', 'ADMIN'),
        ('SALE', 'SALE'),
        ('KHO', 'KHO'),
        ('KE_TOAN', 'KE_TOAN'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Sửa lỗi Reverse Accessor Clashes bằng related_name
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True
    )

    class Meta:
        db_table = 'users'

    @property
    def role_slug(self):
        mapping = {
            'ADMIN': 'admin',
            'SALE': 'sale',
            'KHO': 'kho',
            'KE_TOAN': 'ketoan',
        }
        return mapping.get(self.role, (self.role or '').lower())

    def save(self, *args, **kwargs):
        # 1. Lưu user trước để đảm bảo có ID (đặc biệt quan trọng với UUID)
        is_new = self._state.adding
        super().save(*args, **kwargs)

        # 2. Định nghĩa danh sách quyền cho từng vai trò
        # Cấu trúc: 'CODENAME': 'APP_LABEL'
        ROLE_PERMISSIONS = {
            'KHO': [
                ('view_product', 'product'),
                ('add_product', 'product'),
                ('change_product', 'product'),
                ('view_category', 'product'),
                ('view_productunit', 'product'),
                ('add_productunit', 'product'),
            ],
            'SALE': [
                ('view_product', 'product'),
                ('view_category', 'product'),
                ('view_productunit', 'product'),
                # Sale có thể thêm quyền xem đơn hàng ở đây...
            ],
            'KE_TOAN': [
                ('view_product', 'product'),
                ('view_category', 'product'),      # ← thêm
                ('view_productunit', 'product'),
                # Kế toán có thêm quyền về hóa đơn...
            ]
        }

        # 3. Thực hiện gán quyền nếu không phải ADMIN tối cao
        if self.role in ROLE_PERMISSIONS and not self.is_superuser:
            # Lấy danh sách quyền từ dictionary trên
            perms_to_add = []
            for codename, app_label in ROLE_PERMISSIONS[self.role]:
                try:
                    perm = Permission.objects.get(
                        codename=codename,
                        content_type__app_label=app_label
                    )
                    perms_to_add.append(perm)
                except Permission.DoesNotExist:
                    continue
            
            # Xóa quyền cũ và thêm quyền mới để tránh bị trùng lặp hoặc thừa quyền khi đổi Role
            self.user_permissions.set(perms_to_add)

        # Nếu là ADMIN, cấp toàn bộ quyền staff
        if self.role == 'ADMIN':
            self.is_staff = True
            self.is_superuser = True
            super().save(update_fields=['is_staff', 'is_superuser'])
