from django import forms
from django.core.exceptions import ValidationError
from .models import ImportReceipt, ImportReceiptItem, ExportReceipt, ExportReceiptItem


CONTROL_CLASS = 'search-input'


class ImportReceiptForm(forms.ModelForm):
    """Form tạo/sửa phiếu nhập kho"""
    
    class Meta:
        model = ImportReceipt
        fields = ['note']
        labels = {
            'note': 'Ghi chú'
        }
        widgets = {
            'note': forms.Textarea(attrs={
                'class': CONTROL_CLASS,
                'placeholder': 'Ghi chú về phiếu nhập',
                'rows': 4
            })
        }
    
    def clean_note(self):
        note = self.cleaned_data.get('note')
        if note and len(note) > 500:
            raise ValidationError("Ghi chú không được vượt quá 500 ký tự.")
        return note


class ImportReceiptItemForm(forms.ModelForm):
    """Form tạo/sửa chi tiết phiếu nhập"""
    
    class Meta:
        model = ImportReceiptItem
        fields = ['product', 'quantity', 'unit_price', 'note']
        labels = {
            'product': 'Sản phẩm',
            'quantity': 'Số lượng',
            'unit_price': 'Đơn giá',
            'note': 'Ghi chú'
        }
        widgets = {
            'product': forms.Select(attrs={'class': CONTROL_CLASS}),
            'quantity': forms.NumberInput(attrs={
                'class': CONTROL_CLASS,
                'step': '0.01',
                'min': '0.01'
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': CONTROL_CLASS,
                'step': '0.0001',
                'min': '0'
            }),
            'note': forms.TextInput(attrs={
                'class': CONTROL_CLASS,
                'placeholder': 'Ghi chú chi tiết'
            })
        }
    
    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty and qty <= 0:
            raise ValidationError("Số lượng phải lớn hơn 0.")
        if qty and qty > 999999:
            raise ValidationError("Số lượng quá lớn.")
        return qty
    
    def clean_unit_price(self):
        price = self.cleaned_data.get('unit_price')
        if price and price < 0:
            raise ValidationError("Đơn giá không được âm.")
        if price and price > 9999999:
            raise ValidationError("Đơn giá quá lớn.")
        return price


class ExportReceiptForm(forms.ModelForm):
    """Form tạo/sửa phiếu xuất kho"""
    
    class Meta:
        model = ExportReceipt
        fields = ['note']
        labels = {
            'note': 'Lý do xuất kho'
        }
        widgets = {
            'note': forms.Textarea(attrs={
                'class': CONTROL_CLASS,
                'placeholder': 'Lý do xuất kho, ghi chú',
                'rows': 4
            })
        }
    
    def clean_note(self):
        note = self.cleaned_data.get('note')
        if note and len(note) > 500:
            raise ValidationError("Ghi chú không được vượt quá 500 ký tự.")
        return note


class ExportReceiptItemForm(forms.ModelForm):
    """Form tạo/sửa chi tiết phiếu xuất"""
    
    class Meta:
        model = ExportReceiptItem
        fields = ['product', 'quantity', 'unit_price', 'note']
        labels = {
            'product': 'Sản phẩm',
            'quantity': 'Số lượng',
            'unit_price': 'Đơn giá',
            'note': 'Ghi chú'
        }
        widgets = {
            'product': forms.Select(attrs={'class': CONTROL_CLASS}),
            'quantity': forms.NumberInput(attrs={
                'class': CONTROL_CLASS,
                'step': '0.01',
                'min': '0.01'
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': CONTROL_CLASS,
                'step': '0.0001',
                'min': '0'
            }),
            'note': forms.TextInput(attrs={
                'class': CONTROL_CLASS,
                'placeholder': 'Ghi chú chi tiết'
            })
        }
    
    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty and qty <= 0:
            raise ValidationError("Số lượng phải lớn hơn 0.")
        if qty and qty > 999999:
            raise ValidationError("Số lượng quá lớn.")
        return qty
    
    def clean_unit_price(self):
        price = self.cleaned_data.get('unit_price')
        if price and price < 0:
            raise ValidationError("Đơn giá không được âm.")
        if price and price > 9999999:
            raise ValidationError("Đơn giá quá lớn.")
        return price
