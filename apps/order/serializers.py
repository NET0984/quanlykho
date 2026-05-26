from rest_framework import serializers
from .models import SalesOrder, WarehouseTransaction, Warehouse


class WarehouseSerializer(serializers.ModelSerializer):
    """Serializer cho kho"""
    
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'address']
    
    def validate_name(self, value):
        if value and len(value) < 2:
            raise serializers.ValidationError("Tên kho phải có ít nhất 2 ký tự.")
        return value


class SalesOrderSerializer(serializers.ModelSerializer):
    """Serializer cho đơn hàng bán"""
    
    class Meta:
        model = SalesOrder
        fields = ['id', 'order_code', 'customer_name', 'total_amount', 'status', 'order_date']
    
    def validate_order_code(self, value):
        if value and len(value) < 5:
            raise serializers.ValidationError("Mã đơn hàng phải có ít nhất 5 ký tự.")
        if value and len(value) > 20:
            raise serializers.ValidationError("Mã đơn hàng không được vượt quá 20 ký tự.")
        return value
    
    def validate_customer_name(self, value):
        if value and len(value) < 2:
            raise serializers.ValidationError("Tên khách hàng phải có ít nhất 2 ký tự.")
        if value and len(value) > 100:
            raise serializers.ValidationError("Tên khách hàng không được vượt quá 100 ký tự.")
        return value
    
    def validate_total_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Tổng tiền không được âm.")
        return value


class WarehouseTransactionSerializer(serializers.ModelSerializer):
    """Serializer cho giao dịch kho"""
    
    class Meta:
        model = WarehouseTransaction
        fields = ['id', 'code', 'product', 'warehouse', 'quantity', 'transaction_type', 'transaction_date']
    
    def validate_code(self, value):
        if value and len(value) < 5:
            raise serializers.ValidationError("Mã giao dịch phải có ít nhất 5 ký tự.")
        if value and len(value) > 20:
            raise serializers.ValidationError("Mã giao dịch không được vượt quá 20 ký tự.")
        return value
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Số lượng phải lớn hơn 0.")
        if value > 999999:
            raise serializers.ValidationError("Số lượng quá lớn.")
        return value
    
    def validate_transaction_type(self, value):
        valid_types = ['IMPORT', 'EXPORT', 'ADJUST']
        if value and value.upper() not in valid_types:
            raise serializers.ValidationError(f"Loại giao dịch phải là một trong: {', '.join(valid_types)}")
        return value.upper() if value else value
