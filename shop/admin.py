from django.contrib import admin
from .models import *
from .form import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
# admin.site.register(Product) 
# admin.site.register(Size)
admin.site.register(SubCategory)
# admin.site.register(Color)
admin.site.register(Variant)

admin.site.register(ProductImage)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(Review)
admin.site.register(Payment)


class VariantInline(admin.TabularInline):
    model = Variant
    formset = VariantFormSet

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [VariantInline]

