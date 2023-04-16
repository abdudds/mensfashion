from django import forms
from shop.form import *

class CouponForm(forms.ModelForm):
    active = forms.BooleanField(widget=forms.CheckboxInput(attrs={'style': 'margin-left: 70px;'}))
    class Meta:
        model = Coupon
        fields = ['code', 'discount', 'min_value', 'max_value', 'valid_from', 'valid_to', 'active']
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local','placeholder': 'First Name', 'class':'form-control','style':'max-width:300px; margin-left:115px'}),
            'valid_to': forms.DateTimeInput(attrs={'type': 'datetime-local','placeholder': 'First Name','class':'form-control', 'style':'max-width:300px; margin-left:115px'}),
            'code': forms.TextInput(attrs={'placeholder': 'Coupon code', 'class': 'form-control','style':'max-width:300px; margin-left:115px'}),
            'discount': forms.TextInput(attrs={'placeholder': 'Discount', 'class': 'form-control','style':'max-width:300px; margin-left:115px'}),
            'min_value': forms.TextInput(attrs={'placeholder': 'Minimum value', 'class': 'form-control','style':'max-width:300px; margin-left:115px'}),
            'max_value': forms.TextInput(attrs={'placeholder': 'Maximum value', 'class': 'form-control','style':'max-width:300px; margin-left:115px'}),
        }