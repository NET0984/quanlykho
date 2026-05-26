"""
Django settings cho dự án Quản Lý Kho Vật Liệu
Đã tích hợp: CORS + JWT Authentication (Tuần 7 - Sprint 2)
"""

import os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# BẢO MẬT - Đọc từ .env, KHÔNG hardcode vào đây!
# ============================================================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']  # Giới hạn lại khi deploy production

# ============================================================
# APPS - Thêm corsheaders và rest_framework
# ============================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ✅ CORS - Cho phép Frontend gọi API
    'corsheaders',

    # ✅ Django REST Framework + JWT
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',  # Hỗ trợ logout (vô hiệu hóa token)

    # Apps của dự án
    'apps.authentication',
    'apps.order',           # Đơn hàng
    'apps.warehouse.apps.WarehouseConfig',  # Nhập kho, tồn kho
    'apps.product',
    'apps.inventory.apps.InventoryConfig',  # Kiểm kê & Hao hụt
    'apps.reports',
]

# ============================================================
# MIDDLEWARE - corsheaders PHẢI đứng ĐẦU TIÊN!
# ============================================================
MIDDLEWARE = [
    # ✅ CORS middleware - PHẢI đứng trước tất cả các middleware khác
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 👈 QUAN TRỌNG
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.notifications_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':     os.environ.get('DB_NAME',     'quanlykhovatlieu'),
        'USER':     os.environ.get('DB_USER',     'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '123456'),
        'HOST':     os.environ.get('DB_HOST',     'localhost'),
        'PORT':     os.environ.get('DB_PORT',     '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# User model tùy chỉnh
AUTH_USER_MODEL = 'authentication.User'

# Login URL - Nơi redirect khi user chưa đăng nhập
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'

# ============================================================
# ✅ CORS CONFIGURATION
# Cho phép Frontend (React/Vue/...) gọi API từ domain khác
# ============================================================

# Lấy danh sách domain từ .env (production)
_cors_origins_str = os.environ.get('CORS_ALLOWED_ORIGINS', '')
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in _cors_origins_str.split(',')
    if origin.strip()
] or [
    # Mặc định khi phát triển (development)
    'http://localhost:3000',
    'http://localhost:5173',  # Vite
    'http://localhost:5174',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5173',
]

# Cho phép gửi cookie/credentials cùng request (cần cho một số trường hợp)
CORS_ALLOW_CREDENTIALS = True

# Các HTTP method được phép
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Các header được phép trong request từ Frontend
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',      # ← Quan trọng! Để gửi "Bearer <token>"
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ============================================================
# ✅ DJANGO REST FRAMEWORK CONFIGURATION
# ============================================================
REST_FRAMEWORK = {
    # Mặc định: Mọi API đều yêu cầu đăng nhập (JWT)
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # Định dạng response
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    # Allow business query param `format=excel|pdf` without DRF treating it as renderer override.
    'URL_FORMAT_OVERRIDE': None,
}

# ============================================================
# ✅ JWT CONFIGURATION (theo BM01: token 7 ngày, lưu localStorage)
# ============================================================
SIMPLE_JWT = {
    # Theo BM01: ☑ 7 ngày
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),

    # Refresh token dùng để lấy access token mới (tuỳ chọn)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),

    # Tự động tạo refresh token mới khi dùng refresh endpoint
    'ROTATE_REFRESH_TOKENS': True,

    # Vô hiệu hóa refresh token cũ sau khi rotate (bảo mật cao hơn)
    'BLACKLIST_AFTER_ROTATION': True,

    # Thuật toán mã hóa
    'ALGORITHM': 'HS256',

    # Signing key - dùng SECRET_KEY của Django
    'SIGNING_KEY': os.environ.get('JWT_SECRET_KEY', SECRET_KEY),

    # Theo BM01: Payload chứa userId, hoTen, vaiTro
    # (Cấu hình thêm trong serializer/views)

    # Header name trong HTTP request
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

    # Field trong User model dùng để identify
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# ============================================================
# PASSWORD VALIDATION
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================
# INTERNATIONALISATION
# ============================================================
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
