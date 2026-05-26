"""
apps/product/forms.py - Form với validation đầy đủ
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category, ProductUnit
from .validators import (
    ProductValidator,
    CategoryValidator,
    ProductUnitValidator,
    validate_product_name_unique,
    validate_category_name_unique,
)
from .file_validators import validate_file_image

# Cấu hình chung cho các Input
CONTROL_CLASS = 'search-input'


class CategoryForm(forms.ModelForm):
    """Form tạo/sửa danh mục"""
    
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Tên danh mục'}
        widgets = {
            'name': forms.TextInput(attrs={
                'class': CONTROL_CLASS,
                'placeholder': 'VD: Vật liệu xây dựng, Sắt thép...'
            })
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name) < 2:
            raise ValidationError("Tên danh mục phải có ít nhất 2 ký tự.")
        if name and len(name) > 255:
            raise ValidationError("Tên danh mục không được vượt quá 255 ký tự.")
        return name


class ProductForm(forms.ModelForm):
    """Form tạo/chỉnh sửa sản phẩm với validation đầy đủ"""
    
    # Thêm trường upload ảnh mới (không bắt buộc để có thể sửa sản phẩm mà không cần upload lại)
    anh_san_pham = forms.ImageField(
        required=False,
        label='Ảnh sản phẩm',
        widget=forms.FileInput(attrs={
            'class': 'file-input-hidden',
            'accept': 'image/jpeg,image/png,image/webp',
            'id': 'id_anh_san_pham'
        }),
        error_messages={
            'invalid_image': 'File không phải ảnh hợp lệ.',
        }
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'base_price', 'base_unit']
        labels = {
            'name': 'Tên vật liệu',
            'category': 'Danh mục',
            'base_price': 'Giá cơ bản',
            'base_unit': 'Đơn vị gốc',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'VD: Xi măng Hà Tiên'}),
            'category': forms.Select(attrs={'class': CONTROL_CLASS}),
            'base_price': forms.NumberInput(attrs={'class': CONTROL_CLASS, 'step': '0.01', 'min': '0'}),
            'base_unit': forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'VD: Bao, Cây, m3...'}),
        }
    
    def clean_name(self):
        """Kiểm tra tên sản phẩm"""
        name = self.cleaned_data.get('name')
        
        # Kiểm tra format
        try:
            name = ProductValidator.validate_product_name(name)
        except ValidationError as e:
            raise forms.ValidationError(e.message)
        
        # Kiểm tra trùng lặp (ngoại trừ bản ghi hiện tại khi chỉnh sửa)
        try:
            validate_product_name_unique(name, exclude_id=self.instance.id if self.instance.id else None)
        except ValidationError as e:
            raise forms.ValidationError(e.message)
        
        return name

    def clean_base_price(self):
        """Kiểm tra giá cơ bản"""
        price = self.cleaned_data.get('base_price')
        try:
            price = ProductValidator.validate_base_price(price)
        except ValidationError as e:
            raise forms.ValidationError(e.message)
        return price

    def clean_base_unit(self):
        """Kiểm tra đơn vị cơ bản"""
        unit = self.cleaned_data.get('base_unit')
        try:
            unit = ProductValidator.validate_base_unit(unit)
        except ValidationError as e:
            raise forms.ValidationError(e.message)
        return unit

    def clean_anh_san_pham(self):
        """Kiểm tra file ảnh"""
        file = self.cleaned_data.get('anh_san_pham')
        if file:
            try:
                validate_file_image(file)
            except ValidationError as e:
                raise forms.ValidationError(e.message)
        return file

    def clean(self):
        """Kiểm tra tổng hợp"""
        cleaned_data = super().clean()
        
        # Kiểm tra danh mục được chọn
        category = cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("Vui lòng chọn danh mục.")
        
        return cleaned_data

class ProductUnitForm(forms.ModelForm):
    """Form tạo/sửa đơn vị sản phẩm"""
    
    class Meta:
        model = ProductUnit
        fields = ['product', 'unit_name', 'conversion_rate']
        labels = {
            'product': 'Sản phẩm',
            'unit_name': 'Tên đơn vị',
            'conversion_rate': 'Tỷ lệ chuyển đổi'
        }
        widgets = {
            'product': forms.Select(attrs={'class': CONTROL_CLASS}),
            'unit_name': forms.TextInput(attrs={
                'class': CONTROL_CLASS,
                'placeholder': 'VD: Bao, Cây, m3...'
            }),
            'conversion_rate': forms.NumberInput(attrs={
                'class': CONTROL_CLASS,
                'step': '0.0001',
                'min': '0.0001'
            })
        }
    
    def clean_unit_name(self):
        unit_name = self.cleaned_data.get('unit_name')
        if unit_name and len(unit_name) < 1:
            raise ValidationError("Tên đơn vị không được để trống.")
        return unit_name
    
    def clean_conversion_rate(self):
        rate = self.cleaned_data.get('conversion_rate')
        if rate and rate <= 0:
            raise ValidationError("Tỷ lệ chuyển đổi phải lớn hơn 0.")
        if rate and rate > 1000000:
            raise ValidationError("Tỷ lệ chuyển đổi quá lớn.")
        return rate

class CategoryForm(forms.ModelForm):
    """Form tạo/chỉnh sửa danh mục với validation đầy đủ"""
    
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Tên danh mục'}
        widgets = {
            'name': forms.TextInput(attrs={
                'class': CONTROL_CLASS,
                'placeholder': 'VD: Gạch xây dựng, Sắt thép...'
            }),
        }

    def clean_name(self):
        """Kiểm tra tên danh mục"""
        name = self.cleaned_data.get('name')
        
        # Kiểm tra format
        try:
            name = CategoryValidator.validate_category_name(name)
        except ValidationError as e:
            raise forms.ValidationError(e.message)
        
        # Kiểm tra trùng lặp (ngoại trừ bản ghi hiện tại khi chỉnh sửa)
        try:
            validate_category_name_unique(name, exclude_id=self.instance.id if self.instance.id else None)
        except ValidationError as e:
            raise forms.ValidationError(e.message)
        
        return name


class ProductUnitForm(forms.ModelForm):
    """Form tạo/chỉnh sửa đơn vị sản phẩm với validation đầy đủ"""
    
    class Meta:
        model = ProductUnit
        fields = ['product', 'unit_name', 'conversion_rate']
        labels = {
            'product': 'Sản phẩm mục tiêu',
            'unit_name': 'Đơn vị quy đổi',
            'conversion_rate': 'Tỷ lệ quy đổi'
        }
        widgets = {
            'product': forms.Select(attrs={'class': CONTROL_CLASS}),
            'unit_name': forms.TextInput(attrs={'class': CONTROL_CLASS, 'placeholder': 'VD: Tấn, Thiên, Lốc'}),
            'conversion_rate': forms.NumberInput(attrs={'class': CONTROL_CLASS, 'step': '0.0001', 'min': '0'}),
        }

    def clean_unit_name(self):
        """Kiểm tra tên đơn vị"""
        unit_name = self.cleaned_data.get('unit_name')
        try:
            unit_name = ProductUnitValidator.validate_unit_name(unit_name)
        except ValidationError as e:
            raise forms.ValidationError(e.message)
        return unit_name

    def clean_conversion_rate(self):
        """Kiểm tra tỷ lệ quy đổi"""
        rate = self.cleaned_data.get('conversion_rate')
        try:
            rate = ProductUnitValidator.validate_conversion_rate(rate)
        except ValidationError as e:
            raise forms.ValidationError(e.message)
        return rate

    def clean(self):
        """Kiểm tra tổng hợp"""
        cleaned_data = super().clean()
        return cleaned_data
