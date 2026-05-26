from rest_framework import serializers
from .models import Category, Product, ProductUnit


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        if value and len(value) < 2:
            raise serializers.ValidationError('Tên danh m?c ph?i có ít nh?t 2 ký t?.')
        if value and len(value) > 255:
            raise serializers.ValidationError('Tên danh m?c không du?c vu?t quá 255 ký t?.')
        return value


class ProductUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductUnit
        fields = ['id', 'product', 'unit_name', 'conversion_rate']

    def validate_unit_name(self, value):
        if value and len(value) < 1:
            raise serializers.ValidationError('Tên don v? không du?c d? tr?ng.')
        return value

    def validate_conversion_rate(self, value):
        if value and value <= 0:
            raise serializers.ValidationError('T? l? chuy?n d?i ph?i l?n hon 0.')
        if value and value > 1000000:
            raise serializers.ValidationError('T? l? chuy?n d?i quá l?n.')
        return value


class ProductSerializer(serializers.ModelSerializer):
    units = ProductUnitSerializer(many=True, read_only=True)
    stock_quantity = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    stock_status = serializers.CharField(read_only=True)
    stock_status_label = serializers.CharField(read_only=True)
    total_imported_quantity = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    total_exported_quantity = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    total_ordered_quantity = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'base_price', 'base_unit', 'image_url', 'units',
            'stock_quantity', 'stock_status', 'stock_status_label',
            'total_imported_quantity', 'total_exported_quantity', 'total_ordered_quantity',
        ]

    def validate_name(self, value):
        if value and len(value) < 2:
            raise serializers.ValidationError('Tên s?n ph?m ph?i có ít nh?t 2 ký t?.')
        return value

    def validate_base_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Giá không du?c âm.')
        return value

    def validate_base_unit(self, value):
        if value and len(value) < 1:
            raise serializers.ValidationError('Ðon v? g?c không du?c d? tr?ng.')
        return value

    def validate_image_url(self, value):
        if value and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError('URL hình ?nh ph?i b?t d?u b?ng http:// ho?c https://.')
        return value

