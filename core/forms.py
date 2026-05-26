from django import forms
# from .models import ProductUnits, Products

# class UnitConversionForm(forms.ModelForm):
#     class Meta:
#         model = ProductUnits
#         fields = ['product', 'unit_name', 'conversion_rate']
#         widgets = {
#             'unit_name': forms.TextInput(attrs={'class': 'search-input', 'placeholder': 'Ví dụ: Tấn, Mét khối...'}),
#             'conversion_rate': forms.NumberInput(attrs={'class': 'search-input', 'step': '0.0001'}),
#             'product': forms.Select(attrs={'class': 'search-input'}),
#         }