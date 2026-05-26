from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Count
from .models import Category, Product, ProductUnit

class CategoryRepository:
    @staticmethod
    def get_all():
        """Lấy tất cả danh mục và đếm số sản phẩm trong mỗi danh mục"""
        return Category.objects.annotate(total_products=Count('products')).all().order_by('name')

    @staticmethod
    def get_by_id(category_id):
        return get_object_or_404(Category, pk=category_id)

    @staticmethod
    def create(name):
        return Category.objects.create(name=name)

    @staticmethod
    def update(category, name):
        category.name = name
        category.save()
        return category

    @staticmethod
    def delete(category):
        category.delete()
        return True

class ProductRepository:
    @staticmethod
    def get_all(category_id=None, search_name=None):
        """
        Lấy danh sách sản phẩm. 
        - Dùng select_related để lấy luôn thông tin Category (1 câu lệnh SQL duy nhất).
        - Dùng prefetch_related để lấy danh sách đơn vị quy đổi đính kèm.
        """
        queryset = Product.objects.select_related('category').prefetch_related('units').all()
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if search_name:
            queryset = queryset.filter(name__icontains=search_name)
            
        return queryset.order_by('-name')

    @staticmethod
    def get_by_id(product_id):
        return get_object_or_404(
            Product.objects.select_related('category').prefetch_related('units'), 
            pk=product_id
        )

    @transaction.atomic
    def create_product_with_units(self, product_data, units_data=None):
        """
        Tạo sản phẩm và các đơn vị quy đổi đi kèm trong một giao dịch (Transaction).
        Nếu lỗi ở bất kỳ bước nào, toàn bộ dữ liệu sẽ không được lưu.
        """
        # 1. Tạo sản phẩm chính
        product = Product.objects.create(**product_data)
        
        # 2. Tạo danh sách đơn vị quy đổi (nếu có)
        if units_data:
            unit_instances = [
                ProductUnit(product=product, **unit) 
                for unit in units_data
            ]
            ProductUnit.objects.bulk_create(unit_instances)
            
        return product

    @staticmethod
    def update(product, data):
        for attr, value in data.items():
            setattr(product, attr, value)
        product.save()
        return product

    @staticmethod
    def delete(product):
        product.delete()
        return True

class ProductUnitRepository:

    model = ProductUnit # Khai báo model

    @staticmethod
    def get_all():
        return ProductUnit.objects.select_related('product').all().order_by('product__name')

    def get_by_id(self, unit_id):
        """Lấy một đơn vị quy đổi theo ID (UUID)"""
        return self.model.objects.filter(pk=unit_id).first()

    @staticmethod
    def get_by_product(product_id):
        return ProductUnit.objects.filter(product_id=product_id).order_by('conversion_rate')

    @staticmethod
    def create(data):
        return ProductUnit.objects.create(**data)

    @staticmethod
    def update(unit, data):
        for attr, value in data.items():
            setattr(unit, attr, value)
        unit.save()
        return unit

    @staticmethod
    def delete(unit_id):
        unit = ProductUnit.objects.filter(pk=unit_id).first()
        if unit:
            unit.delete()
            return True
        return False