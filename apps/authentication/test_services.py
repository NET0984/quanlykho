from django.test import TestCase, RequestFactory
from django.contrib.auth import authenticate
from .models import User
from .services import UserService
from .repositories import UserRepository


class TestUserServiceLogin(TestCase):
    """Test login_service method"""
    
    def setUp(self):
        """Khởi tạo dữ liệu test"""
        self.service = UserService()
        self.factory = RequestFactory()
        # Tạo người dùng test
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            role='ADMIN'
        )
    
    def test_login_service_success(self):
        """Test login thành công"""
        request = self.factory.get('/')
        user = self.service.login_service(request, 'testuser', 'testpass123')
        
        # Kiểm tra người dùng được trả về
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')
    
    def test_login_service_wrong_password(self):
        """Test login với mật khẩu sai"""
        request = self.factory.get('/')
        user = self.service.login_service(request, 'testuser', 'wrongpassword')
        
        # Kiểm tra không có người dùng được trả về
        self.assertIsNone(user)
    
    def test_login_service_nonexistent_user(self):
        """Test login với tài khoản không tồn tại"""
        request = self.factory.get('/')
        user = self.service.login_service(request, 'nonexistent', 'password')
        
        # Kiểm tra không có người dùng được trả về
        self.assertIsNone(user)
    
    def test_login_service_inactive_user(self):
        """Test login với tài khoản bị vô hiệu hóa"""
        # Vô hiệu hóa người dùng
        self.user.is_active = False
        self.user.save()
        
        request = self.factory.get('/')
        user = self.service.login_service(request, 'testuser', 'testpass123')
        
        # Kiểm tra không thể login tài khoản vô hiệu hóa
        self.assertIsNone(user)


class TestUserServiceCreateNewStaff(TestCase):
    """Test create_new_staff method"""
    
    def setUp(self):
        """Khởi tạo dữ liệu test"""
        self.service = UserService()
    
    def test_create_new_staff_with_password(self):
        """Test tạo nhân viên với mật khẩu"""
        data = {
            'username': 'newstaff',
            'email': 'staff@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'KHO',
            'password': 'SecurePass123'
        }
        
        user = self.service.create_new_staff(data)
        
        # Kiểm tra người dùng được tạo
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'newstaff')
        self.assertEqual(user.role, 'KHO')
        
        # Kiểm tra mật khẩu được băm đúng
        self.assertTrue(user.check_password('SecurePass123'))
    
    def test_create_new_staff_without_password(self):
        """Test tạo nhân viên mà không có mật khẩu"""
        data = {
            'username': 'newstaff2',
            'email': 'staff2@example.com',
            'role': 'SALE'
            # Không có password
        }
        
        user = self.service.create_new_staff(data)
        
        # Kiểm tra được tạo với mật khẩu mặc định
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('TeLiet@123'))
    
    def test_create_new_staff_password_hashed(self):
        """Test rằng mật khẩu được băm, không là plaintext"""
        data = {
            'username': 'teststaff',
            'email': 'test@example.com',
            'role': 'KE_TOAN',
            'password': 'MyPassword123'
        }
        
        user = self.service.create_new_staff(data)
        
        # Kiểm tra mật khẩu không được lưu dưới dạng plaintext
        self.assertNotEqual(user.password, 'MyPassword123')
        # Kiểm tra mật khẩu được băm
        self.assertTrue(user.password.startswith('pbkdf2_sha256'))


class TestUserServiceUpdatePassword(TestCase):
    """Test update_password method"""
    
    def setUp(self):
        """Khởi tạo dữ liệu test"""
        self.service = UserService()
        self.user = User.objects.create_user(
            username='updatetest',
            password='oldpass123',
            email='update@example.com',
            role='ADMIN'
        )
    
    def test_update_password_success(self):
        """Test đổi mật khẩu thành công"""
        user_id = self.user.id
        success, message = self.service.update_password(
            user_id, 
            'oldpass123', 
            'newpass456'
        )
        
        # Kiểm tra cập nhật thành công
        self.assertTrue(success)
        self.assertEqual(message, 'Đổi mật khẩu thành công.')
        
        # Kiểm tra mật khẩu mới được lưu
        updated_user = User.objects.get(id=user_id)
        self.assertTrue(updated_user.check_password('newpass456'))
    
    def test_update_password_wrong_old_password(self):
        """Test đổi mật khẩu với mật khẩu cũ sai"""
        user_id = self.user.id
        success, message = self.service.update_password(
            user_id, 
            'wrongoldpass', 
            'newpass456'
        )
        
        # Kiểm tra không thành công
        self.assertFalse(success)
        self.assertEqual(message, 'Mật khẩu cũ không chính xác.')
        
        # Kiểm tra mật khẩu cũ vẫn hoạt động
        updated_user = User.objects.get(id=user_id)
        self.assertTrue(updated_user.check_password('oldpass123'))
    
    def test_update_password_user_not_found(self):
        """Test đổi mật khẩu với user không tồn tại"""
        fake_id = '99999999-9999-9999-9999-999999999999'
        success, message = self.service.update_password(
            fake_id, 
            'oldpass', 
            'newpass'
        )
        
        # Kiểm tra không tìm thấy user
        self.assertFalse(success)
        self.assertEqual(message, 'Không tìm thấy người dùng.')


class TestUserServiceGetProfile(TestCase):
    """Test get_profile method"""
    
    def setUp(self):
        """Khởi tạo dữ liệu test"""
        self.service = UserService()
        self.user = User.objects.create_user(
            username='profiletest',
            email='profile@example.com',
            first_name='John',
            last_name='Smith',
            role='KHO',
            full_name='John Smith',
            phone_number='0123456789',
            address='123 Street, City'
        )
    
    def test_get_profile_success(self):
        """Test lấy profil thành công"""
        user_id = self.user.id
        profile = self.service.get_profile(user_id)
        
        # Kiểm tra lấy được đúng user
        self.assertIsNotNone(profile)
        self.assertEqual(profile.username, 'profiletest')
        self.assertEqual(profile.role, 'KHO')
        self.assertEqual(profile.full_name, 'John Smith')
    
    def test_get_profile_not_found(self):
        """Test lấy profil user không tồn tại"""
        fake_id = '99999999-9999-9999-9999-999999999999'
        profile = self.service.get_profile(fake_id)
        
        # Kiểm tra trả về None
        self.assertIsNone(profile)
