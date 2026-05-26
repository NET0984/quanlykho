import logging
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from apps.core.exceptions import LoiTuyChon

logger = logging.getLogger(__name__)
User = get_user_model()

class XuLyLoiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        # Log lỗi ra console để dev theo dõi
        logger.error(f"❌ Lỗi: {exception}", exc_info=True)

        # Nếu là lỗi tùy chọn của chúng ta
        if isinstance(exception, LoiTuyChon):
            return JsonResponse({
                'thanhCong': False,
                'maLoi': exception.ma_loi,
                'thongBao': exception.thong_bao,
                'chiTiet': exception.chi_tiet
            }, status=exception.ma_http)

        # Lỗi không mong đợi (ví dụ lỗi code, lỗi DB)
        return JsonResponse({
            'thanhCong': False,
            'maLoi': 'INTERNAL_ERROR',
            'thongBao': 'Đã xảy ra lỗi, vui lòng thử lại sau'
        }, status=500)


# ============================================================
# JWT Authentication Middleware
# Tự động xác thực user từ JWT token trong Authorization header
# Cho phép dùng cả Session auth và JWT auth
# ============================================================
class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        # Nếu user chưa authenticated bằng session, thử authentication bằng JWT
        if not request.user.is_authenticated:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            
            if auth_header.startswith('Bearer '):
                try:
                    # Verify JWT token
                    validated_token = self.jwt_auth.get_validated_token(auth_header[7:])
                    user = self.jwt_auth.get_user(validated_token)
                    request.user = user
                    logger.debug(f"✅ JWT Authentication thành công: {user.username}")
                except (InvalidToken, AuthenticationFailed) as e:
                    logger.warning(f"❌ JWT Authentication thất bại: {e}")
                    pass  # Nếu không valid, để user là AnonymousUser

        return self.get_response(request)