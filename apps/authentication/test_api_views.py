from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class AuthenticationApiTests(APITestCase):
    def setUp(self):
        self.username = 'api_tester'
        self.password = 'OldPass@123'
        self.new_password = 'NewPass@123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            full_name='API Tester',
            role='KHO',
            email='api_tester@example.com',
        )

    def _login(self, username=None, password=None):
        return self.client.post(
            '/api/xac-thuc/',
            {
                'username': username or self.username,
                'password': password or self.password,
            },
            format='json',
        )

    @staticmethod
    def _auth_header(access_token):
        return {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

    def test_login_returns_expected_payload(self):
        response = self._login()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data.get('userId'), str(self.user.id))
        self.assertEqual(response.data.get('hoTen'), self.user.full_name)
        self.assertEqual(response.data.get('vaiTro'), self.user.role)

    def test_login_rejects_wrong_password(self):
        response = self._login(password='SaiMatKhau!')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)

    def test_profile_requires_token(self):
        response = self.client.get('/api/xac-thuc/profile/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_returns_current_user(self):
        login_response = self._login()
        access_token = login_response.data['access']

        response = self.client.get(
            '/api/xac-thuc/profile/',
            **self._auth_header(access_token),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('userId'), str(self.user.id))
        self.assertEqual(response.data.get('username'), self.username)
        self.assertEqual(response.data.get('hoTen'), self.user.full_name)
        self.assertEqual(response.data.get('vaiTro'), self.user.role)

    def test_change_password_rejects_wrong_old_password(self):
        login_response = self._login()
        access_token = login_response.data['access']

        response = self.client.put(
            '/api/xac-thuc/changepass/',
            {'old_password': 'wrong_old_password', 'new_password': self.new_password},
            format='json',
            **self._auth_header(access_token),
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message'), 'Mật khẩu cũ không chính xác')

    def test_change_password_updates_password(self):
        login_response = self._login()
        access_token = login_response.data['access']

        change_response = self.client.put(
            '/api/xac-thuc/changepass/',
            {'old_password': self.password, 'new_password': self.new_password},
            format='json',
            **self._auth_header(access_token),
        )

        self.assertEqual(change_response.status_code, status.HTTP_200_OK)
        self.assertEqual(change_response.data.get('message'), 'Đổi mật khẩu thành công')

        old_login = self._login(password=self.password)
        new_login = self._login(password=self.new_password)

        self.assertEqual(old_login.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(new_login.status_code, status.HTTP_200_OK)

    def test_refresh_returns_new_access_token(self):
        login_response = self._login()
        refresh_token = login_response.data['refresh']

        response = self.client.post(
            '/api/xac-thuc/refresh/',
            {'refresh': refresh_token},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_logout_blacklists_refresh_token(self):
        login_response = self._login()
        access_token = login_response.data['access']
        refresh_token = login_response.data['refresh']

        logout_response = self.client.post(
            '/api/xac-thuc/logout/',
            {'refresh_token': refresh_token},
            format='json',
            **self._auth_header(access_token),
        )

        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

        refresh_again_response = self.client.post(
            '/api/xac-thuc/refresh/',
            {'refresh': refresh_token},
            format='json',
        )

        self.assertIn(
            refresh_again_response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED],
        )


class CorsConfigurationTests(TestCase):
    def test_preflight_allows_configured_origin(self):
        allowed_origin = 'http://localhost:5173'
        response = self.client.options(
            '/api/xac-thuc/',
            HTTP_ORIGIN=allowed_origin,
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='POST',
            HTTP_ACCESS_CONTROL_REQUEST_HEADERS='authorization,content-type',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.headers.get('Access-Control-Allow-Origin'),
            allowed_origin,
        )
        self.assertEqual(
            response.headers.get('Access-Control-Allow-Credentials'),
            'true',
        )
        allow_headers = response.headers.get('Access-Control-Allow-Headers', '').lower()
        self.assertIn('authorization', allow_headers)

    def test_preflight_rejects_unlisted_origin(self):
        blocked_origin = 'http://khong-duoc-phep.local'
        response = self.client.options(
            '/api/xac-thuc/',
            HTTP_ORIGIN=blocked_origin,
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='POST',
            HTTP_ACCESS_CONTROL_REQUEST_HEADERS='authorization,content-type',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(
            response.headers.get('Access-Control-Allow-Origin'),
            blocked_origin,
        )