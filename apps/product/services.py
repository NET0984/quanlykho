from .repositories import ProductRepository, CategoryRepository, ProductUnitRepository

from decimal import Decimal


def _normalize_name(value):

    return (value or '').strip().casefold()



class ProductService:

    def __init__(self):

        self.repository = ProductRepository()

        self.unit_repository = ProductUnitRepository()



    def get_all_products(self, search=None, category=None):

        return self.repository.get_all(category_id=category, search_name=search)



    def create_product(self, data, units=None):

        """

        Logic nghiệp vụ khi tạo sản phẩm:

        - Đảm bảo tên sản phẩm viết hoa chữ cái đầu.

        - Gọi Repository để lưu sản phẩm và các đơn vị quy đổi.

        """

        if 'name' in data:

            data['name'] = data['name'].strip().title()

        

        return self.repository.create_product_with_units(data, units)



    def calculate_price_by_unit(self, product_id, unit_id):

        """

        Logic quan trọng: Tính giá bán dựa trên đơn vị quy đổi.

        Công thức: Giá cơ bản * Tỷ lệ quy đổi

        Ví dụ: Xi măng 100k/bao, 1 tấn = 20 bao -> Giá tấn = 100k * 20 = 2 triệu.

        """

        product = self.repository.get_by_id(product_id)

        unit = self.unit_repository.get_by_product(product_id).filter(id=unit_id).first()

        

        if not unit:

            return product.base_price # Nếu không có đơn vị quy đổi, trả về giá gốc

            

        return product.base_price * unit.conversion_rate



    def add_new_unit_to_product(self, product_id, unit_name, conversion_rate):

        """

        Kiểm tra nếu đơn vị đã tồn tại thì không cho thêm trùng tên.

        """

        existing_units = self.unit_repository.get_by_product(product_id)
        normalized_unit_name = _normalize_name(unit_name)

        if any(_normalize_name(unit.unit_name) == normalized_unit_name for unit in existing_units):

            return None, "Đơn vị này đã tồn tại cho sản phẩm này."

        

        unit_data = {

            'product_id': product_id,

            'unit_name': unit_name,

            'conversion_rate': Decimal(conversion_rate)

        }

        return self.unit_repository.create(unit_data), "Thành công"



class CategoryService:

    def __init__(self):

        self.repository = CategoryRepository()



    def get_list(self):

        return self.repository.get_all()



    def create_category(self, name):

        """Logic kiểm tra và tạo danh mục"""

        if not name:

            return None, "Tên danh mục không được để trống."

        normalized_name = _normalize_name(name)
        if not normalized_name:
            return None, "Tên danh mục không được để trống."

            

        # Kiểm tra trùng tên (không phân biệt hoa thường)

        from .models import Category

        if any(_normalize_name(category_name) == normalized_name for category_name in Category.objects.values_list('name', flat=True)):

            return None, f"Danh mục '{name}' đã tồn tại trong hệ thống."

            

        category = self.repository.create(name=name.strip())

        return category, "Thành công"