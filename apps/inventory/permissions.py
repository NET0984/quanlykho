"""
apps/inventory/permissions.py
==============================
DRF permission classes for the inventory module.
Follows the same role convention as the rest of the project:
  ADMIN, KHO, SALE, KE_TOAN
"""

from rest_framework.permissions import BasePermission


def _role(user):
    """Return the effective role string, treating superusers as ADMIN."""
    if getattr(user, 'is_superuser', False):
        return 'ADMIN'
    return getattr(user, 'role', '')


class IsAdminRole(BasePermission):
    """Only ADMIN (including superuser)."""
    message = 'Chỉ quản trị viên mới có quyền thực hiện thao tác này.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and _role(request.user) == 'ADMIN'


class IsKhoOrAdmin(BasePermission):
    """KHO và ADMIN — tạo phiếu kiểm kê, ghi số thực tế."""
    message = 'Chỉ Thủ kho hoặc Quản trị viên mới có quyền.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and _role(request.user) in ('KHO', 'ADMIN')


class IsKeToanOrAdmin(BasePermission):
    """KE_TOAN và ADMIN — duyệt / từ chối phiếu kiểm kê và hao hụt."""
    message = 'Chỉ Kế toán hoặc Quản trị viên mới có quyền duyệt.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and _role(request.user) in ('KE_TOAN', 'ADMIN')


class IsKhoOrKeToanOrAdmin(BasePermission):
    """KHO, KE_TOAN, ADMIN — xem báo cáo, danh sách kiểm kê."""
    message = 'Bạn không có quyền xem dữ liệu này.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and _role(request.user) in ('KHO', 'KE_TOAN', 'ADMIN')


class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission: chỉ người tạo hoặc ADMIN mới sửa được.
    Dùng trong has_object_permission().
    """
    message = 'Bạn không có quyền sửa đổi bản ghi này.'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        role = _role(request.user)
        if role == 'ADMIN':
            return True
        created_by = getattr(obj, 'created_by_id', None) or getattr(obj, 'created_by', None)
        if hasattr(created_by, 'pk'):
            return created_by.pk == request.user.pk
        return created_by == request.user.pk
