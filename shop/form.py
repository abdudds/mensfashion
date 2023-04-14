from django import forms
from .models import *
from django.forms import inlineformset_factory

class VariantStockForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['stock']

    # def clean_stock(self):
    #     stock = self.cleaned_data['stock']
    #     print(stock, '++++++++++==============================================')
    #     if stock < 0:
    #         raise forms.ValidationError('Stock cannot be negative')
    #     return stock

    # def save(self, commit=True):
    #     variant = super().save(commit=False)
    #     print(variant, '+++++++++++++++++===============================')
    #     variant.product.stock -= variant.stock - variant.pk.stock
    #     if commit:
    #         variant.product.save()
    #         variant.save()
    #     return variant
    
VariantFormSet = inlineformset_factory(
    Product, Variant, form=VariantStockForm, extra=0
)



