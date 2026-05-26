from .models import User

class UserRepository:
    @staticmethod
    def get_by_id(user_id):
        """Tìm người dùng theo UUID"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_by_username(username):
        """Tìm người dùng theo tên đăng nhập"""
        return User.objects.filter(username=username).first()

    @staticmethod
    def get_all_active_users():
        """Lấy danh sách nhân viên đang hoạt động"""
        return User.objects.filter(is_active=True).order_by('-date_joined')

    @staticmethod
    def create_user_instance(user_data):
        """Khởi tạo một đối tượng User trong bộ nhớ (chưa lưu)"""
        return User(**user_data)

    @staticmethod
    def save(user_instance):
        """Lưu đối tượng User vào Database"""
        user_instance.save()
        return user_instance

    @staticmethod
    def delete(user_instance):
        """Xóa người dùng (hoặc chuyển is_active=False)"""
        user_instance.is_active = False
        user_instance.save()