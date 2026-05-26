from rest_framework import serializers

from .models import ExportReceipt, ExportReceiptItem, ImportReceipt, ImportReceiptItem, ProductStock
from .stock_utils import get_stock_status_label


class ImportReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportReceiptItem
        fields = ['id', 'product', 'quantity', 'unit_price', 'note']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('S? lu?ng ph?i l?n hon 0.')
        if value > 999999:
            raise serializers.ValidationError('S? lu?ng quá l?n.')
        return value

    def validate_unit_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Ðon giá không du?c âm.')
        if value > 9999999:
            raise serializers.ValidationError('Ðon giá quá l?n.')
        return value


class ImportReceiptSerializer(serializers.ModelSerializer):
    items = ImportReceiptItemSerializer(many=True, read_only=True)

    class Meta:
        model = ImportReceipt
        fields = ['id', 'receipt_code', 'status', 'note', 'created_at', 'items']

    def validate_note(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError('Ghi chú không du?c vu?t quá 500 ký t?.')
        return value


class ExportReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportReceiptItem
        fields = ['id', 'product', 'quantity', 'unit_price', 'note']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('S? lu?ng ph?i l?n hon 0.')
        if value > 999999:
            raise serializers.ValidationError('S? lu?ng quá l?n.')
        return value

    def validate_unit_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Ðon giá không du?c âm.')
        if value > 9999999:
            raise serializers.ValidationError('Ðon giá quá l?n.')
        return value


class ExportReceiptSerializer(serializers.ModelSerializer):
    items = ExportReceiptItemSerializer(many=True, read_only=True)
    sales_order_code = serializers.CharField(source='sales_order.order_code', read_only=True)

    class Meta:
        model = ExportReceipt
        fields = ['id', 'receipt_code', 'status', 'note', 'created_at', 'sales_order_code', 'items']

    def validate_note(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError('Ghi chú không du?c vu?t quá 500 ký t?.')
        return value


class ProductStockSerializer(serializers.ModelSerializer):
    stock_status = serializers.SerializerMethodField()

    class Meta:
        model = ProductStock
        fields = ['id', 'product', 'quantity', 'stock_status', 'last_updated']

    def get_stock_status(self, obj):
        return get_stock_status_label(obj.quantity)

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError('S? lu?ng không du?c âm.')
        return value
