from django.db import models
from users.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

COLOR_CHOICES = (
    ('White','White'),
    ('Black','Black'),
    ('Green','Green'),
    ('Red','Red'),
    ('Yellow','Yellow'),
    ('Blue','Blue'),
    ('Brown','Brown'),
    ('Orange','Orange'),
)

SIZE_CHOICES = (
    ('XS','XS'),
    ('S','S'),
    ('M','M'),
    ('L','L'),
    ('XL','XL'),
    ('XXL','XXL'),
    ('XXXL','XXXL'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
)

######### Product Models
class Category(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='company')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # stock = models.PositiveBigIntegerField(default=0)
    image = models.ImageField(upload_to='products', default='product_images/default.jpg')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variant')
    color = models.CharField(choices=COLOR_CHOICES,max_length=20)
    size = models.CharField(choices=SIZE_CHOICES,max_length=20)
    stock = models.PositiveIntegerField(default=0)  
    
    def __str__(self):
        return self.product.name  

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveIntegerField(default=0)
    user_review = models.TextField(blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Product-Images', default='product_images/default.jpg')

    def __str__(self):
        return self.product.name
    
#Wish List#    
class WishList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name    
    
#Cart#

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.product.name
    
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(500)])
    min_value = models.IntegerField(validators=[MinValueValidator(0)])
    max_value = models.IntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=False)

    def _str_(self):
        return self.code

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=30, null=True, blank=True)
    payment_id = models.CharField(max_length=30, null=True, blank=True)
    refund_id = models.CharField(max_length=30, null=True, blank=True)
    order_id = models.CharField(max_length=100,blank=True,default='empty')
    payment_method = models.CharField(max_length=100)
    amount_paid = models.FloatField(default=0)
    paid = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def str(self):
        return self.order_id

class Order(models.Model):
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped',"Shipped"),
        ('Out for delivery',"Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    order_no = models.IntegerField(unique=True)
    order_date = models.DateField(auto_now_add=True)
    delivery_address = models.ForeignKey(Address,on_delete=models.CASCADE)
    discount = models.FloatField(default=0)
    refund_completed = models.BooleanField(default=False)
    order_total = models.FloatField(null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50,choices=STATUS,default='Order Confirmed')

    def __str__(self):
        return str(self.order_no)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.variant.product.name