import re
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from .models import Product, Category

# =========================
# PRODUCT VALIDATOR
# =========================
class ProductValidator:

    @staticmethod
    def validate_product_name(name):
        # Sửa "không được rỗng" thành "không được để trống" để khớp logic test
        if not name or not str(name).strip():
            raise ValidationError("không được để trống")

        name = str(name).strip()

        if len(name) < 3:
            raise ValidationError("ít nhất 3 ký tự")

        if len(name) > 255:
            raise ValidationError("vượt quá 255 ký tự")

        if re.search(r'[<>]', name):
            raise ValidationError("Tên sản phẩm chứa ký tự không hợp lệ")

        return name

    @staticmethod
    def validate_base_price(price):
        try:
            price_val = Decimal(str(price))
        except (InvalidOperation, ValueError, TypeError):
            raise ValidationError("phải là một số")

        # Kiểm tra số âm trước (để pass test_validate_base_price_negative)
        if price_val < 0:
            raise ValidationError("không được là số âm")
            
        # Sau đó kiểm tra số 0 (để pass test_validate_base_price_zero)
        if price_val == 0:
            raise ValidationError("lớn hơn 0")

        return price_val

    @staticmethod
    def validate_base_unit(unit):
        if not unit or not str(unit).strip():
            raise ValidationError("không được để trống")

        unit = str(unit).strip()

        if len(unit) > 50:
            raise ValidationError("vượt quá 50 ký tự")

        return unit

    # Giữ nguyên validate_create/update nhưng cập nhật message cho đồng bộ
    @staticmethod
    def validate_create(data: dict) -> dict:
        errors = {}
        try:
            ProductValidator.validate_product_name(data.get('name', ''))
        except ValidationError as e:
            errors['name'] = str(e.message)

        base_price = data.get('base_price')
        try:
            ProductValidator.validate_base_price(base_price)
        except ValidationError as e:
            errors['base_price'] = str(e.message)

        try:
            ProductValidator.validate_base_unit(data.get('base_unit', ''))
        except ValidationError as e:
            errors['base_unit'] = str(e.message)

        return errors

    @staticmethod
    def validate_update(data: dict) -> dict:
        errors = {}
        if 'name' in data:
            try: ProductValidator.validate_product_name(data['name'])
            except ValidationError as e: errors['name'] = str(e.message)
        
        if 'base_price' in data:
            try: ProductValidator.validate_base_price(data['base_price'])
            except ValidationError as e: errors['base_price'] = str(e.message)

        if 'base_unit' in data:
            try: ProductValidator.validate_base_unit(data['base_unit'])
            except ValidationError as e: errors['base_unit'] = str(e.message)
            
        return errors


# =========================
# CATEGORY VALIDATOR
# =========================
class CategoryValidator:

    @staticmethod
    def validate_category_name(name):
        if not name or not str(name).strip():
            raise ValidationError("không được để trống")

        name = str(name).strip()

        if len(name) < 2:
            raise ValidationError("ít nhất 2 ký tự")

        if re.search(r'[<>]', name):
            raise ValidationError("Tên danh mục chứa ký tự không hợp lệ")

        return name

    @staticmethod
    def validate_create(data: dict) -> dict:
        errors = {}
        try:
            CategoryValidator.validate_category_name(data.get('name', ''))
        except ValidationError as e:
            errors['name'] = str(e.message)
        return errors

    @staticmethod
    def validate_update(data: dict) -> dict:
        return CategoryValidator.validate_create(data)


# =========================
# PRODUCT UNIT VALIDATOR
# =========================
class ProductUnitValidator:

    @staticmethod
    def validate_unit_name(name):
        if not name or not str(name).strip():
            raise ValidationError("không được để trống")
        return name

    @staticmethod
    def validate_conversion_rate(rate):
        try:
            rate_val = Decimal(str(rate))
        except (InvalidOperation, ValueError, TypeError):
            raise ValidationError("phải là một số")

        if rate_val <= 0:
            raise ValidationError("lớn hơn 0")

        return rate_val

    @staticmethod
    def validate_create(data: dict) -> dict:
        errors = {}
        try:
            ProductUnitValidator.validate_unit_name(data.get('unit_name', ''))
        except ValidationError as e:
            errors['unit_name'] = str(e.message)

        try:
            ProductUnitValidator.validate_conversion_rate(data.get('conversion_rate'))
        except ValidationError as e:
            errors['conversion_rate'] = str(e.message)

        return errors

    @staticmethod
    def validate_update(data: dict) -> dict:
        return ProductUnitValidator.validate_create(data)


# =========================
# UNIQUE & FILE VALIDATION
# =========================
def validate_product_name_unique(value, exclude_id=None):
    qs = Product.objects.filter(name__iexact=value.strip())
    if exclude_id:
        qs = qs.exclude(id=exclude_id)
    if qs.exists():
        raise ValidationError("Tên sản phẩm đã tồn tại")
    return value

def validate_category_name_unique(value):
    if Category.objects.filter(name__iexact=value.strip()).exists():
        raise ValidationError("Tên danh mục đã tồn tại")

def validate_file_image(file):
    if not file: return
    if file.size > 5 * 1024 * 1024:
        raise ValidationError("Ảnh vượt quá 2MB")
    valid_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
    if file.content_type not in valid_types:
        raise ValidationError("Chỉ chấp nhận JPG, JPEG, PNG")
