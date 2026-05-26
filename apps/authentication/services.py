from django.contrib.auth import authenticate

from .repositories import UserRepository



class UserService:

    def __init__(self):

        self.repository = UserRepository()



    def login_service(self, request, username, password):

        """

        Xác thực người dùng.

        Tận dụng hàm authenticate() của Django: 

        - Kiểm tra mật khẩu (đã băm)

        - Kiểm tra tài khoản có bị khóa không (is_active)

        """

        user = authenticate(request, username=username, password=password)

        return user



    def create_new_staff(self, data):

        """

        Tạo nhân viên mới an toàn.

        Tận dụng hàm set_password() của Django Model.

        """

        raw_password = data.pop('password', None)

        

        # 1. Khởi tạo instance từ dữ liệu thô

        user = self.repository.create_user_instance(data)

        

        # 2. Băm mật khẩu bằng thuật toán PBKDF2 của Django

        if raw_password:

            user.set_password(raw_password)

        else:

            # Nếu không nhập, đặt mật khẩu mặc định hoặc báo lỗi

            user.set_password("TeLiet@123")

            

        # 3. Lưu thông qua Repository

        return self.repository.save(user)



    def update_password(self, user_id, old_password, new_password):

        """

        Đổi mật khẩu an toàn.

        Tận dụng check_password() và set_password().

        """

        user = self.repository.get_by_id(user_id)

        if not user:

            return False, "Không tìm thấy người dùng."



        # Kiểm tra mật khẩu cũ (Django tự băm rồi so sánh)

        if not user.check_password(old_password):

            return False, "Mật khẩu cũ không chính xác."



        # Cập nhật mật khẩu mới

        user.set_password(new_password)

        self.repository.save(user)

        return True, "Đổi mật khẩu thành công."



    def get_profile(self, user_id):

        """Lấy thông tin chi tiết nhân viên"""

        return self.repository.get_by_id(user_id)

