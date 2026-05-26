from django import forms
from django.core.exceptions import ValidationError
from .models import SalesOrder, WarehouseTransaction


CONTROL_CLASS = 'search-input'


class SalesOrderForm(forms.ModelForm):
    """Form tạo/sửa đơn hàng bán"""
    
    class Meta:
        model = SalesOrder
        fields = ['order_code', 'customer_name', 'total_amount', 'status']
        labels = {
            'order_code': 'Mã đơn hàng',
            'customer_name': 'Tên khách hàng',
            'total_amount': 'Tổng tiền',
            'status': 'Trạng thái'
        }
        widgets = {
            'order_code': forms.TextInput(attrs={
                'class': CONTROL_CLASS,
                'placeholder': 'VD: ORD-001'
            }),
            'customer_name': forms.TextInput(attrs={
                'class': CONTROL_CLASS,
                'placeholder': 'Tên khách hàng'
            }),
            'total_amount': forms.NumberInput(attrs={
                'class': CONTROL_CLASS,
                'step': '0.01',
                'min': '0'
            }),
            'status': forms.Select(attrs={'class': CONTROL_CLASS})
        }
    
    def clean_order_code(self):
        code = self.cleaned_data.get('order_code')
        if code and len(code) < 5:
            raise ValidationError("Mã đơn hàng phải có ít nhất 5 ký tự.")
        if code and len(code) > 20:
            raise ValidationError("Mã đơn hàng không được vượt quá 20 ký tự.")
        return code
    
    def clean_customer_name(self):
        name = self.cleaned_data.get('customer_name')
        if name and len(name) < 2:
            raise ValidationError("Tên khách hàng phải có ít nhất 2 ký tự.")
        if name and len(name) > 100:
            raise ValidationError("Tên khách hàng không được vượt quá 100 ký tự.")
        return name
    
    def clean_total_amount(self):
        amount = self.cleaned_data.get('total_amount')
        if amount and amount < 0:
            raise ValidationError("Tổng tiền không được âm.")
        return amount


class WarehouseTransactionForm(forms.ModelForm):
    """Form tạo/sửa giao dịch kho"""
    
    class Meta:
        model = WarehouseTransaction
        fields = ['code', 'product', 'warehouse', 'quantity', 'transaction_type']
        labels = {
            'code': 'Mã giao dịch',
            'product': 'Sản phẩm',
            'warehouse': 'Kho',
            'quantity': 'Số lượng',
            'transaction_type': 'Loại giao dịch'
        }
        widgets = {
            'code': forms.TextInput(attrs={
                'class': CONTROL_CLASS,
                'placeholder': 'VD: TXN-001'
            }),
            'product': forms.Select(attrs={'class': CONTROL_CLASS}),
            'warehouse': forms.Select(attrs={'class': CONTROL_CLASS}),
            'quantity': forms.NumberInput(attrs={
                'class': CONTROL_CLASS,
                'step': '0.01',
                'min': '0.01'
            }),
            'transaction_type': forms.TextInput(attrs={
                'class': CONTROL_CLASS,
                'placeholder': 'IMPORT/EXPORT/ADJUST'
            })
        }
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code and len(code) < 5:
            raise ValidationError("Mã giao dịch phải có ít nhất 5 ký tự.")
        if code and len(code) > 20:
            raise ValidationError("Mã giao dịch không được vượt quá 20 ký tự.")
        return code
    
    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty and qty <= 0:
            raise ValidationError("Số lượng phải lớn hơn 0.")
        if qty and qty > 999999:
            raise ValidationError("Số lượng quá lớn.")
        return qty
    
    def clean_transaction_type(self):
        trans_type = self.cleaned_data.get('transaction_type')
        valid_types = ['IMPORT', 'EXPORT', 'ADJUST']
        if trans_type and trans_type.upper() not in valid_types:
            raise ValidationError(f"Loại giao dịch phải là một trong: {', '.join(valid_types)}")
        return trans_type.upper() if trans_type else trans_type
