"""
Serializers cho Authentication - theo BM01
Payload JWT chứa: userId, hoTen, vaiTro (theo BM01 mục 2 ☑)
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# ============================================================
# JWT CUSTOM PAYLOAD - Thêm hoTen, vaiTro vào token (theo BM01)
# ============================================================
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Ghi đè token mặc định để thêm userId, hoTen, vaiTro vào payload.
    Theo BM01 mục 2: ☑ userId  ☑ hoTen  ☑ vaiTro
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Thêm các trường tùy chỉnh vào payload JWT
        token['userId'] = str(user.id)
        token['hoTen'] = user.full_name or user.username
        token['vaiTro'] = user.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Thêm thông tin người dùng vào response body (ngoài token)
        # Response theo BM01: { "access": "...", "refresh": "...", "vaiTro": "..." }
        data['vaiTro'] = self.user.role
        data['userId'] = str(self.user.id)
        data['hoTen'] = self.user.full_name or self.user.username

        return data


# ============================================================
# PROFILE SERIALIZER - Trả về thông tin cá nhân theo BM01
# Response: { "userId": 1, "username": "...", "hoTen": "...", "vaiTro": "..." }
# ============================================================
class UserProfileSerializer(serializers.ModelSerializer):
    hoTen = serializers.CharField(source='full_name')
    vaiTro = serializers.CharField(source='role')
    userId = serializers.UUIDField(source='id')

    class Meta:
        model = User
        fields = ['userId', 'username', 'hoTen', 'vaiTro', 'phone_number', 'email']
        read_only_fields = fields


# ============================================================
# CHANGE PASSWORD SERIALIZER - Đổi mật khẩu theo BM01
# Request: { "old_password": "...", "new_password": "..." }
# ============================================================
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=6)
    # Backward compatible: older clients only send old_password/new_password.
    new_password_confirm = serializers.CharField(required=False, write_only=True, min_length=6, allow_blank=False)

    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Mật khẩu mới phải có ít nhất 6 ký tự.")
        if len(value) > 128:
            raise serializers.ValidationError("Mật khẩu quá dài.")
        return value
    
    def validate(self, data):
        new_password_confirm = data.get('new_password_confirm')
        if new_password_confirm is not None and data.get('new_password') != new_password_confirm:
            raise serializers.ValidationError({"new_password": "Mật khẩu mới không khớp."})
        return data


# ============================================================
# USER CREATE SERIALIZER - Tạo người dùng mới
# ============================================================
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'phone_number', 'password', 'password_confirm', 'role']
    
    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Tên đăng nhập phải có ít nhất 3 ký tự.")
        if len(value) > 150:
            raise serializers.ValidationError("Tên đăng nhập không được vượt quá 150 ký tự.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Tên đăng nhập đã tồn tại.")
        return value
    
    def validate_full_name(self, value):
        if value and len(value) < 2:
            raise serializers.ValidationError("Họ tên phải có ít nhất 2 ký tự.")
        if value and len(value) > 100:
            raise serializers.ValidationError("Họ tên không được vượt quá 100 ký tự.")
        return value
    
    def validate_phone_number(self, value):
        if value:
            if not value.isdigit():
                raise serializers.ValidationError("Số điện thoại chỉ được chứa chữ số.")
            if len(value) < 10 or len(value) > 11:
                raise serializers.ValidationError("Số điện thoại phải có 10-11 chữ số.")
        return value
    
    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({"password": "Mật khẩu không khớp."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(**validated_data)
        return user


# ============================================================
# USER UPDATE SERIALIZER - Cập nhật thông tin người dùng
# ============================================================
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'address']
    
    def validate_full_name(self, value):
        if value and len(value) < 2:
            raise serializers.ValidationError("Họ tên phải có ít nhất 2 ký tự.")
        if value and len(value) > 100:
            raise serializers.ValidationError("Họ tên không được vượt quá 100 ký tự.")
        return value
    
    def validate_phone_number(self, value):
        if value:
            if not value.isdigit():
                raise serializers.ValidationError("Số điện thoại chỉ được chứa chữ số.")
            if len(value) < 10 or len(value) > 11:
                raise serializers.ValidationError("Số điện thoại phải có 10-11 chữ số.")
        return value
