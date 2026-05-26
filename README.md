Tổng Kết: Tích Hợp CORS & JWT Authentication
Dự án: Quản Lý Kho Vật Liệu Xây Dựng — Nhóm Tê Liệt
Tài liệu gốc: BM01_Luong_Xac_Thuc.md + Slide Tuần 7
Ngày thực hiện: 01/04/2026

1. CORS Là Gì & Đã Làm Gì?
CORS là gì?
CORS (Cross-Origin Resource Sharing) là cơ chế bảo mật của trình duyệt. Khi Frontend (ví dụ React chạy ở localhost:5173) muốn gọi API từ Backend (localhost:8000) — hai cái này khác nguồn gốc (khác port) — trình duyệt sẽ CHẶN request.

CORS cho phép Backend "cấp phép" rõ ràng: "Frontend ở địa chỉ X được phép gọi API của tôi".

NOTE

Postman gọi API được mà trình duyệt không gọi được → Đó là do trình duyệt áp dụng chính sách Same-Origin, Postman thì không.

Đã cấu hình gì?
File: 
requirements.txt
django-cors-headers>=4.3.0    ← Thư viện CORS cho Django
Tác dụng: Cài package django-cors-headers để Django có khả năng xử lý CORS.

File: 
settings.py
INSTALLED_APPS (dòng 34):

python
'corsheaders',    # Kích hoạt app CORS
Tác dụng: Đăng ký app corsheaders với Django, để Django biết sử dụng nó.

MIDDLEWARE (dòng 51):

python
'corsheaders.middleware.CorsMiddleware',    # ĐẦU TIÊN trong danh sách!
Tác dụng: Middleware này đứng đầu tiên để chặn/cho phép request ngay từ đầu, trước tất cả xử lý khác. Nếu đặt sai vị trí → CORS không hoạt động.

CORS_ALLOWED_ORIGINS (dòng 104–116):

python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',     # React mặc định
    'http://localhost:5173',     # Vite
    'http://localhost:5174',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5173',
]
Tác dụng: Chỉ các Frontend từ những địa chỉ này mới được gọi API. Địa chỉ khác → bị chặn. Production thì đọc từ biến .env.

CORS_ALLOW_CREDENTIALS (dòng 119):

python
CORS_ALLOW_CREDENTIALS = True
Tác dụng: Cho phép Frontend gửi cookie/token kèm request.

CORS_ALLOW_METHODS (dòng 122–129):

python
['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
Tác dụng: Cho phép Frontend dùng tất cả các phương thức HTTP cần thiết.

CORS_ALLOW_HEADERS (dòng 132–141):

python
'authorization',    # ← QUAN TRỌNG! Cho phép gửi "Bearer <token>"
'content-type',
Tác dụng: Cho phép Frontend gửi header Authorization: Bearer <token> trong request. Nếu thiếu → Frontend không gửi được JWT token.

2. JWT Là Gì & Đã Làm Gì?
JWT là gì?
JWT (JSON Web Token) là chuỗi mã hóa chứa thông tin người dùng, được tạo khi đăng nhập thành công. Giống như "vé xem phim":

Chứa thông tin: userId, tên, vai trò
Có thời hạn: hết hạn sau 7 ngày
Có chữ ký số: server xác minh được, không ai làm giả được
Không cần database: server chỉ cần verify chữ ký, không cần truy vấn DB mỗi lần
Luồng hoạt động:
Người dùng nhập username + password
        ↓
Frontend gửi POST /api/xac-thuc/ {username, password}
        ↓
Backend kiểm tra: tài khoản tồn tại? mật khẩu đúng?
        ↓
Backend tạo JWT chứa {userId, hoTen, vaiTro}
        ↓
Backend trả về {access token, refresh token, vaiTro}
        ↓
Frontend lưu token vào localStorage
        ↓
Mọi request sau gửi kèm: Authorization: Bearer <token>
        ↓
Backend verify token → Cho phép truy cập
Đã cấu hình gì?
File: 
requirements.txt
djangorestframework>=3.14.0              ← Framework tạo REST API
djangorestframework-simplejwt>=5.3.0     ← Thư viện JWT cho Django
File: 
settings.py
INSTALLED_APPS (dòng 37–39):

python
'rest_framework',                          # Django REST Framework
'rest_framework_simplejwt',                # JWT Authentication
'rest_framework_simplejwt.token_blacklist', # Blacklist (để logout vô hiệu hóa token)
Tác dụng: Kích hoạt REST API + JWT + Blacklist (cho phép vô hiệu hóa token khi logout).

REST_FRAMEWORK (dòng 147–158):

python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
Tác dụng:

Mọi API mặc định yêu cầu đăng nhập (JWT) mới truy cập được
Nếu API nào công khai (như login) → phải ghi đè AllowAny
SIMPLE_JWT (dòng 164–192):

python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),    # BM01: ☑ 7 ngày
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.environ.get('JWT_SECRET_KEY', SECRET_KEY),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
Tác dụng:

Cấu hình	Ý nghĩa
ACCESS_TOKEN_LIFETIME = 7 ngày	Token hết hạn sau 7 ngày (theo BM01)
REFRESH_TOKEN_LIFETIME = 30 ngày	Refresh token dùng để lấy access token mới
ROTATE_REFRESH_TOKENS = True	Khi refresh → tạo refresh token mới luôn
BLACKLIST_AFTER_ROTATION = True	Vô hiệu hóa refresh token cũ (bảo mật hơn)
ALGORITHM = HS256	Thuật toán mã hóa chữ ký
SIGNING_KEY	Key bí mật từ .env để ký token
AUTH_HEADER_TYPES = Bearer	Frontend gửi Authorization: Bearer <token>
3. Các File Đã Tạo Mới
serializers.py
 — [MỚI]
Chứa 3 serializer:

Class	Tác dụng
CustomTokenObtainPairSerializer	Ghi đè JWT mặc định → thêm userId, hoTen, vaiTro vào payload token VÀ response body
UserProfileSerializer	Chuyển đổi User model → JSON theo format BM01: { userId, username, hoTen, vaiTro }
ChangePasswordSerializer	Xác thực input đổi mật khẩu: { old_password, new_password }, yêu cầu tối thiểu 6 ký tự
api_views.py
 — [MỚI]
Chứa 4 API views, đúng 4 endpoint của BM01 mục 1:

View	Endpoint	Method	Tác dụng
LoginAPIView	/api/xac-thuc/	POST	Nhận {username, password}, kiểm tra DB, trả về {access, refresh, vaiTro, hoTen, userId}
LogoutAPIView	/api/xac-thuc/logout/	POST	Nhận {refresh_token}, đưa vào blacklist → token không dùng được nữa
UserProfileAPIView	/api/xac-thuc/profile/	GET	Yêu cầu Bearer Token, trả về thông tin cá nhân người đang đăng nhập
ChangePasswordAPIView	/api/xac-thuc/changepass/	PUT	Yêu cầu Bearer Token + {old_password, new_password}, kiểm tra mật khẩu cũ rồi đổi mới
urls.py
 — [MỚI]
Kết nối 4 API views + 1 endpoint refresh:

/api/xac-thuc/           → LoginAPIView       (POST - Đăng nhập)
/api/xac-thuc/logout/    → LogoutAPIView      (POST - Đăng xuất)
/api/xac-thuc/profile/   → UserProfileAPIView (GET  - Thông tin cá nhân)
/api/xac-thuc/changepass/→ ChangePasswordAPIView (PUT - Đổi mật khẩu)
/api/xac-thuc/refresh/   → TokenRefreshView   (POST - Lấy access token mới)
4. Các File Đã Chỉnh Sửa
core/urls.py
 — [SỬA]
diff
+    # API Xác thực (Theo BM01)
+    path('api/xac-thuc/', include('apps.authentication.urls')),
Tác dụng: Gắn tất cả API xác thực vào URL chính của dự án.

requirements.txt
 — [SỬA]
diff
+python-dotenv>=1.0.0
Tác dụng: Thêm thư viện đọc file .env mà settings.py đang sử dụng.

.env
 — [SỬA]
diff
+SECRET_KEY=HZ3dpJFt_m-8Jjn4...
+JWT_SECRET_KEY=H7FuJvjBu1AFA868...
Tác dụng: Thêm key bí mật cho Django và JWT. Được tạo ngẫu nhiên bằng secrets.token_urlsafe(50).

5. Bảng Kiểm Tra Đối Chiếu BM01
Mục 1 — API Xác thực ✅
Endpoint BM01	Method	Đã có?	File
/api/xac-thuc/	POST	✅	api_views.py → LoginAPIView
/api/xac-thuc/logout	POST	✅	api_views.py → LogoutAPIView
/api/xac-thuc/profile	GET	✅	api_views.py → UserProfileAPIView
/api/xac-thuc/changepass	PUT	✅	api_views.py → ChangePasswordAPIView
Mục 2 — Cấu trúc Token JWT ✅
Yêu cầu BM01	Giá trị	Đã có?
Payload chứa userId	☑	✅ serializers.py dòng 26
Payload chứa hoTen	☑	✅ serializers.py dòng 27
Payload chứa vaiTro	☑	✅ serializers.py dòng 28
Thời hạn token	☑ 7 ngày	✅ settings.py dòng 166
Lưu trữ token	☑ localStorage	⏳ Frontend xử lý
Mục 3 — Phân quyền người dùng ✅
Vai trò	Đã có trong Model?
ADMIN	✅ models.py ROLE_CHOICES
KE_TOAN (Kế toán)	✅ models.py ROLE_CHOICES
KHO (Thủ kho)	✅ models.py ROLE_CHOICES
SALE	✅ models.py ROLE_CHOICES
Mục 4 — Luồng xác thực ✅
Bước	Đã triển khai?
1. Người dùng nhập tài khoản và mật khẩu	✅ LoginAPIView nhận {username, password}
2. Frontend gửi POST /api/xac-thuc/	✅ URL đã cấu hình
3. Backend kiểm tra tài khoản + mật khẩu	✅ SimpleJWT tự kiểm tra qua Django auth
4. Backend tạo JWT chứa {userId, hoTen, vaiTro}	✅ CustomTokenObtainPairSerializer
5. Backend trả về {token, nguoiDung}	✅ Response: {access, refresh, vaiTro, hoTen}
6. Frontend lưu token vào localStorage	⏳ Frontend xử lý
7. Các request sau gửi kèm token trong header	✅ Backend accept Authorization: Bearer xxx
8. Backend xác minh token → cho phép truy cập	✅ JWTAuthentication mặc định cho tất cả API
CORS — Slide Tuần 7 ✅
Yêu cầu	Đã có?
Cài cors package	✅ django-cors-headers
Cấu hình cho phép nguồn cụ thể	✅ CORS_ALLOWED_ORIGINS
credentials: true	✅ CORS_ALLOW_CREDENTIALS = True
Cho phép header Authorization	✅ CORS_ALLOW_HEADERS
CORS middleware đứng đầu tiên	✅ Đầu danh sách MIDDLEWARE
Bảo mật — Slide Tuần 7 ✅
Quy tắc	Đã thực hiện?
Hash mật khẩu (bcrypt/PBKDF2)	✅ Django set_password() tự hash
Dùng file .env cho secrets	✅ SECRET_KEY, JWT_SECRET_KEY trong .env
Thêm .env vào .gitignore	✅ .gitignore dòng 3
Đặt thời hạn token (7 ngày)	✅ ACCESS_TOKEN_LIFETIME = 7d
Không ghi SECRET trong code	✅ Đọc từ os.environ.get()
6. Tổng Kết
Hạng mục	Kết quả
🌐 CORS	✅ ĐỦ — 7/7 yêu cầu
🔑 JWT Cấu hình	✅ ĐỦ — 8/8 yêu cầu
📦 JWT Payload	✅ ĐỦ — 3/3 trường (userId, hoTen, vaiTro)
🌐 API Endpoints	✅ ĐỦ — 4/4 endpoint theo BM01
🔒 Bảo mật	✅ ĐỦ — 5/5 quy tắc
📁 File .env & .gitignore	✅ ĐỦ
IMPORTANT

Kết luận: Backend đã đủ 100% yêu cầu CORS & JWT theo BM01 và Slide Tuần 7.

7. Cấu Trúc File Thay Đổi
TeLiet_Quanlykho/
├── .env                              ← [SỬA] Thêm SECRET_KEY, JWT_SECRET_KEY
├── .gitignore                        ← [ĐÃ CÓ] .env đã được ignore ✅
├── requirements.txt                  ← [SỬA] Thêm python-dotenv
├── core/
│   ├── settings.py                   ← [ĐÃ CÓ] CORS + JWT đã cấu hình ✅
│   └── urls.py                       ← [SỬA] Thêm path('api/xac-thuc/')
└── apps/
    └── authentication/
        ├── models.py                 ← [ĐÃ CÓ] User model với role ✅
        ├── serializers.py            ← [MỚI] Custom JWT payload + Profile + ChangePass
        ├── api_views.py              ← [MỚI] 4 API: Login, Logout, Profile, ChangePass
        └── urls.py                   ← [MỚI] 5 URL patterns cho authentication API
