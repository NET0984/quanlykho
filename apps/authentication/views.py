from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 1. Lấy dữ liệu từ Form gửi lên
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')

        # 2. XÁC THỰC: Django sẽ check trong DB xem user/pass có khớp không
        user = authenticate(request, username=user_name, password=pass_word)

        # 3. KIỂM TRA: Đây là bước quan trọng nhất
        if user is not None:
            # Nếu ĐÚNG: Tạo phiên đăng nhập và chuyển hướng
            login(request, user)
            return redirect('dashboard') 
        else:
            # Nếu SAI: Trả về trang login kèm thông báo lỗi
            # KHÔNG ĐƯỢC redirect ở đây, phải render lại trang login
            return render(request, 'login.html', {
                'error_msg': 'Tên đăng nhập hoặc mật khẩu không chính xác!',
                'old_username': user_name
            })