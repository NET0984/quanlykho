from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from .models import User


class TaiKhoanLoginForm(AuthenticationForm):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'field-input',
            'placeholder': 'Tên đăng nhập',
            'required': 'required'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'field-input',
            'placeholder': 'Mật khẩu',
            'required': 'required'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username or not password:
            raise forms.ValidationError("Vui lòng nhập đầy đủ thông tin.")
        
        if len(username) < 3:
            raise forms.ValidationError("Tên đăng nhập phải có ít nhất 3 ký tự.")
        
        if len(password) < 6:
            raise forms.ValidationError("Mật khẩu phải có ít nhất 6 ký tự.")

        return cleaned_data


class UserCreationFormCustom(UserCreationForm):
    """Form tạo người dùng mới"""
    
    class Meta:
        model = User
        fields = ['username', 'full_name', 'phone_number', 'email', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'field-input', 'placeholder': 'Tên đăng nhập'}),
            'full_name': forms.TextInput(attrs={'class': 'field-input', 'placeholder': 'Họ tên'}),
            'phone_number': forms.TextInput(attrs={'class': 'field-input', 'placeholder': '0123456789'}),
            'email': forms.EmailInput(attrs={'class': 'field-input', 'placeholder': 'user@example.com'}),
            'role': forms.Select(attrs={'class': 'field-input'}),
        }
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if full_name and len(full_name) < 2:
            raise forms.ValidationError("Họ tên phải có ít nhất 2 ký tự.")
        return full_name
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Số điện thoại chỉ được chứa chữ số.")
        if phone and (len(phone) < 10 or len(phone) > 11):
            raise forms.ValidationError("Số điện thoại phải có 10-11 chữ số.")
        return phone


class UserChangeFormCustom(UserChangeForm):
    """Form sửa thông tin người dùng"""
    
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'email', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'field-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'field-input'}),
            'email': forms.EmailInput(attrs={'class': 'field-input'}),
            'address': forms.Textarea(attrs={'class': 'field-input', 'rows': 3}),
        }
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Số điện thoại chỉ được chứa chữ số.")
        if phone and (len(phone) < 10 or len(phone) > 11):
            raise forms.ValidationError("Số điện thoại phải có 10-11 chữ số.")
        return phone