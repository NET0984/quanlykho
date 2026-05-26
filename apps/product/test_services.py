from django.test import TestCase
from decimal import Decimal
from .models import Category, Product, ProductUnit
from .services import ProductService, CategoryService


class TestProductServiceGetAllProducts(TestCase):
    """Test get_all_products method"""
    
    def setUp(self):
        """Khởi tạo dữ liệu test"""
        self.service = ProductService()
        
        # Tạo danh mục
        self.category_xang = Category.objects.create(name='Xăng')
        self.category_dung_cu = Category.objects.create(name='Dụng cụ')
        
        # Tạo sản phẩm
        self.product1 = Product.objects.create(
            name='Xăng 92',
            base_price=Decimal('25000'),
            base_unit='Lít',
            category=self.category_xang
        )
        self.product2 = Product.objects.create(
            name='Dầu nhớt',
            base_price=Decimal('50000'),
            base_unit='Lít',
            category=self.category_xang
        )
        self.product3 = Product.objects.create(
            name='Búa',
            base_price=Decimal('100000'),
            base_unit='Cái',
            category=self.category_dung_cu
        )
    
    def test_get_all_products_no_filter(self):
        """Test lấy tất cả sản phẩm không lọc"""
        products = self.service.get_all_products()
        
        # Kiểm tra có 3 sản phẩm
        self.assertEqual(products.count(), 3)
    
    def test_get_all_products_filter_by_category(self):
        """Test lấy sản phẩm theo danh mục"""
        products = self.service.get_all_products(category=self.category_xang.id)
        
        # Kiểm tra chỉ có sản phẩm trong danh mục Xăng
        self.assertEqual(products.count(), 2)
        for product in products:
            self.assertEqual(product.category.id, self.category_xang.id)
    
    def test_get_all_products_search_by_name(self):
        """Test tìm kiếm sản phẩm theo tên"""
        products = self.service.get_all_products(search='Xăng')
        
        # Kiểm tra tìm thấy sản phẩm có tên chứa 'Xăng'
        self.assertEqual(products.count(), 1)
        self.assertEqual(products[0].name, 'Xăng 92')
    
    def test_get_all_products_filter_and_search(self):
        """Test lấy sản phẩm với cả lọc danh mục và tìm kiếm"""
        products = self.service.get_all_products(
            category=self.category_xang.id,
            search='Dầu'
        )
        
        # Kiểm tra tìm thấy sản phẩm
        self.assertEqual(products.count(), 1)
        self.assertEqual(products[0].name, 'Dầu nhớt')


class TestProductServiceCreateProduct(TestCase):
    """Test create_product method"""
    
    def setUp(self):
        """Khởi tạo dữ liệu test"""
        self.service = ProductService()
        self.category = Category.objects.create(name='Xi măng')
    
    def test_create_product_simple(self):
        """Test tạo sản phẩm đơn giản"""
        data = {
            'name': 'xi măng portland',
            'base_price': Decimal('50000'),
            'base_unit': 'Bao',
            'category_id': self.category.id
        }
        
        product = self.service.create_product(data)
        
        # Kiểm tra sản phẩm được tạo
        self.assertIsNotNone(product)
        # Kiểm tra tên được viết hoa chữ cái đầu
        self.assertEqual(product.name, 'Xi Măng Portland')
    
    def test_create_product_with_units(self):
        """Test tạo sản phẩm với đơn vị quy đổi"""
        data = {
            'name': 'sắt thép',
            'base_price': Decimal('100000'),
            'base_unit': 'Kg',
            'category_id': self.category.id
        }
        units = [
            {'unit_name': 'Tấn', 'conversion_rate': Decimal('1000')},
            {'unit_name': 'Tạ', 'conversion_rate': Decimal('100')}
        ]
        
        product = self.service.create_product(data, units=units)
        
        # Kiểm tra sản phẩm được tạo
        self.assertIsNotNone(product)
        # Kiểm tra có 2 đơn vị quy đổi
        self.assertEqual(product.units.count(), 2)
    
    def test_create_product_name_normalization(self):
        """Test rằng tên sản phẩm được chuẩn hóa (strip + title)"""
        data = {
            'name': '  sơn màu bạc  ',
            'base_price': Decimal('75000'),
            'base_unit': 'Lít',
            'category_id': self.category.id
        }
        
        product = self.service.create_product(data)
        
        # Kiểm tra tên được chuẩn hóa
        self.assertEqual(product.name, 'Sơn Màu Bạc')


class TestProductServiceCalculatePriceByUnit(TestCase):
    """Test calculate_price_by_unit method"""
    
    def setUp(self):
        """Khởi tạo dữ liệu test"""
        self.service = ProductService()
        self.category = Category.objects.create(name='Vật liệu')
        
        # Tạo sản phẩm cơ bản
        self.product = Product.objects.create(
            name='Xi măng',
            base_price=Decimal('100000'),  # 100k/bao
            base_unit='Bao',
            category=self.category
        )
        
        # Tạo đơn vị quy đổi
        self.unit_ton = ProductUnit.objects.create(
            product=self.product,
            unit_name='Tấn',
            conversion_rate=Decimal('20')  # 1 tấn = 20 bao
        )
        self.unit_kg = ProductUnit.objects.create(
            product=self.product,
            unit_name='Kg',
            conversion_rate=Decimal('0.05')  # 1 kg = 0.05 bao
        )
    
    def test_calculate_price_with_conversion(self):
        """Test tính giá với đơn vị quy đổi"""
        price = self.service.calculate_price_by_unit(self.product.id, self.unit_ton.id)
        
        # Kiểm tra công thức: 100,000 * 20 = 2,000,000
        self.assertEqual(price, Decimal('2000000'))
    
    def test_calculate_price_small_unit(self):
        """Test tính giá với đơn vị nhỏ hơn"""
        price = self.service.calculate_price_by_unit(self.product.id, self.unit_kg.id)
        
        # Kiểm tra công thức: 100,000 * 0.05 = 5,000
        self.assertEqual(price, Decimal('5000'))
    
    def test_calculate_price_nonexistent_unit(self):
        """Test tính giá với đơn vị không tồn tại"""
        fake_unit_id = '99999999-9999-9999-9999-999999999999'
        price = self.service.calculate_price_by_unit(self.product.id, fake_unit_id)
        
        # Kiểm tra trả về giá gốc
        self.assertEqual(price, self.product.base_price)


class TestProductServiceAddNewUnitToProduct(TestCase):
    """Test add_new_unit_to_product method"""
    
    def setUp(self):
        """Khởi tạo dữ liệu test"""
        self.service = ProductService()
        self.category = Category.objects.create(name='Sản phẩm')
        
        self.product = Product.objects.create(
            name='Gạch',
            base_price=Decimal('50000'),
            base_unit='Viên',
            category=self.category
        )
        
        # Tạo sẵn một đơn vị
        ProductUnit.objects.create(
            product=self.product,
            unit_name='Chục',
            conversion_rate=Decimal('10')
        )
    
    def test_add_new_unit_success(self):
        """Test thêm đơn vị mới thành công"""
        unit, message = self.service.add_new_unit_to_product(
            self.product.id,
            'Thùng',
            Decimal('100')
        )
        
        # Kiểm tra thêm thành công
        self.assertIsNotNone(unit)
        self.assertEqual(message, 'Thành công')
        self.assertEqual(unit.unit_name, 'Thùng')
        self.assertEqual(unit.conversion_rate, Decimal('100'))
    
    def test_add_duplicate_unit_name(self):
        """Test thêm đơn vị trùng tên"""
        unit, message = self.service.add_new_unit_to_product(
            self.product.id,
            'Chục',  # Tên đơn vị đã tồn tại
            Decimal('10')
        )
        
        # Kiểm tra không thành công
        self.assertIsNone(unit)
        self.assertIn('đã tồn tại', message)
    
    def test_add_unit_case_insensitive(self):
        """Test kiểm tra trùng tên không phân biệt hoa thường"""
        unit, message = self.service.add_new_unit_to_product(
            self.product.id,
            'CHỤC',  # Khác hoa thường nhưng cùng tên
            Decimal('10')
        )
        
        # Kiểm tra không thành công (kiểm tra không phân biệt hoa thường)
        self.assertIsNone(unit)
        self.assertIn('đã tồn tại', message)


class TestCategoryServiceGetList(TestCase):
    """Test get_list method của CategoryService"""
    
    def setUp(self):
        """Khởi tạo dữ liệu test"""
        self.service = CategoryService()
        
        # Tạo danh mục test
        self.category1 = Category.objects.create(name='A - Danh mục 1')
        self.category2 = Category.objects.create(name='B - Danh mục 2')
        self.category3 = Category.objects.create(name='C - Danh mục 3')
    
    def test_get_list_returns_all_categories(self):
        """Test lấy tất cả danh mục"""
        categories = self.service.get_list()
        
        # Kiểm tra có 3 danh mục
        self.assertEqual(categories.count(), 3)
    
    def test_get_list_ordered_by_name(self):
        """Test danh mục được sắp xếp theo tên"""
        categories = self.service.get_list()
        names = [cat.name for cat in categories]
        
        # Kiểm tra sắp xếp theo tên A -> B -> C
        expected_names = ['A - Danh mục 1', 'B - Danh mục 2', 'C - Danh mục 3']
        self.assertEqual(names, expected_names)


class TestCategoryServiceCreateCategory(TestCase):
    """Test create_category method của CategoryService"""
    
    def setUp(self):
        """Khởi tạo dữ liệu test"""
        self.service = CategoryService()
    
    def test_create_category_success(self):
        """Test tạo danh mục thành công"""
        category, message = self.service.create_category('Điện tử')
        
        # Kiểm tra tạo thành công
        self.assertIsNotNone(category)
        self.assertEqual(message, 'Thành công')
        self.assertEqual(category.name, 'Điện tử')
        
        # Kiểm tra lưu vào database
        self.assertTrue(Category.objects.filter(name='Điện tử').exists())
    
    def test_create_category_empty_name(self):
        """Test tạo danh mục với tên rỗng"""
        category, message = self.service.create_category('')
        
        # Kiểm tra không thành công
        self.assertIsNone(category)
        self.assertIn('không được để trống', message)
    
    def test_create_category_duplicate_name(self):
        """Test tạo danh mục với tên đã tồn tại"""
        # Tạo danh mục đầu tiên
        Category.objects.create(name='Xây dựng')
        
        # Cố gắng tạo danh mục cùng tên
        category, message = self.service.create_category('Xây dựng')
        
        # Kiểm tra không thành công
        self.assertIsNone(category)
        self.assertIn('đã tồn tại', message)
    
    def test_create_category_case_insensitive(self):
        """Test kiểm tra trùng tên không phân biệt hoa thường"""
        # Tạo danh mục
        Category.objects.create(name='Nước')
        
        # Cố gắng tạo danh mục khác hoa thường
        category, message = self.service.create_category('NƯỚC')
        
        # Kiểm tra không thành công (kiểm tra không phân biệt hoa thường)
        self.assertIsNone(category)
        self.assertIn('đã tồn tại', message)
    
    def test_create_category_name_stripped(self):
        """Test rằng tên danh mục được loại bỏ khoảng trắng đầu cuối"""
        category, message = self.service.create_category('  Nội thất  ')
        
        # Kiểm tra tên được loại bỏ khoảng trắng
        self.assertEqual(category.name, 'Nội thất')
