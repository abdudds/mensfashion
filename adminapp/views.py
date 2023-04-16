from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from users.form import UserLoginForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from users.models import User
from shop.models import *
from django.core.paginator import Paginator
from django.db.models import Sum
from django.urls import reverse_lazy
from datetime import date
from .form import CouponForm
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate
# Create your views here.

class AdminLoginView(LoginView): 
    template_name = 'adminapp/login.html'
    form_class = UserLoginForm
    extra_context ={'title' : 'Login-admin'}
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        return self.success_url
    
class AdminLogoutView(LogoutView):
    next_page = '/adminapp/'

def super_user_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_active and user.is_staff,
        login_url='adminapp-login')(view_func)
    
    return decorated_view_func


class DashboardView(PermissionRequiredMixin, TemplateView): 
    template_name = 'adminapp/index.html'
    permission_required = 'is_superuser'

    
    try:
        user_count = User.objects.all().count()
        order_count = Order.objects.all().count()
        todays_order = Order.objects.filter(order_date=date.today()).count()
        todays_income = round(Payment.objects.filter(created_at=date.today()).aggregate(Sum('amount_paid'))['amount_paid__sum'],2)

    except:
        user_count = 0
        order_count = 0
        todays_order = 0
        todays_income = 0
    
    try:
        cod_income = round(Payment.objects.filter(payment_method='cash on delivery', paid=True).aggregate(Sum('amount_paid'))['amount_paid__sum'],2)
        cod_pending = round(Payment.objects.filter(payment_method='cash on delivery').aggregate(Sum('amount_paid'))['amount_paid__sum'],2) - cod_income
        payments = Payment.objects.all()
        total_sale = round(sum(float(payment.amount_paid) for payment in payments if payment.amount_paid),2)
        razor_income = round(Payment.objects.filter(payment_method='razorpay').aggregate(Sum('amount_paid'))['amount_paid__sum'],2)
        cod_percent = round(cod_income*100/total_sale, 2)
        pending_percent = round(cod_pending*100/total_sale, 2)
        razor_percent = round(razor_income*100/total_sale, 2)
    
    except:
        cod_income = 0
        cod_pending = 0
        payments = None
        total_sale = 0
        razor_income = 0
        cod_percent = 0
        pending_percent = 0
        razor_percent = 0
    
    # total_sale = Payment.objects.all().aggregate(sum('amount_paid'))['amount_paid__sum']
    

    last_month = datetime.now() - timedelta(days=30)

    daily_income = (
        Payment.objects.filter(created_at__gte=last_month)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(total_income=Sum('amount_paid'))
        .order_by('date')
    )

    extra_context ={
        'title' : 'Dasboard-admin', 
        'user_count': user_count,
        'order_count': order_count,
        'todays_income': todays_income,
        'total_sale': total_sale,
        'cod_income': cod_income,
        'razor_income': razor_income,
        'cod_pending': cod_pending,
        'cod_percent': cod_percent,
        'pending_percent': pending_percent,
        'razor_percent': razor_percent,
        'daily_income': daily_income,
        'todays_order': todays_order,
        'last_month': last_month
        }


@super_user_required
def sales_report(request):
    fro=request.GET.get('from_date')
    to=request.GET.get('to_date')
    
    if fro and to :
        orders = Order.objects.all().order_by('-id')
        today_date = datetime.now().strftime('%Y-%m-%d')

        if 'from_date' in request.GET and 'to_date' in request.GET:
            from_date = request.GET['from_date']
            to_date = request.GET['to_date']

            if to_date > today_date:
                messages.warning(request, "Please select a date up to today's date.")
            elif from_date > to_date:
                messages.warning(request, "The from date should be before than the To date")
            else:
                orders = orders.filter(order_date__range=[from_date, to_date])
                # total_sales = orders.aggregate(Sum('paid_amount'))['paid_amount__sum']
    else:
        orders = Order.objects.all().order_by('-id')
       
       
    return render(request, 'adminapp/sales.html', locals())

@super_user_required
def category(request): 
    categorys = Category.objects.filter(is_active=True)
    return render(request, 'adminapp/category.html', {'categorys': categorys})

@super_user_required
def add_category(request):
    if request.method == 'POST':
        Category.objects.create(name=request.POST['category'])
    return render(request, 'adminapp/add_category.html')

@super_user_required
def edit_category(request, cat_id):
    try:
        category = Category.objects.get(id=cat_id)
    except:
        category = None
    if request.method == 'POST':
        category.name=request.POST['category']
        category.save()
        return redirect('category')
    else:
        return render(request, 'adminapp/add_category.html', {'category': category})

@super_user_required
def del_category(request, cat_id):
    try:
        category = Category.objects.get(id=cat_id)
        category.is_active = False
        category.save()
    except:
        category = None
    
    return redirect('category')

@super_user_required
def sub_category(request): 
    sub_categorys = SubCategory.objects.filter(is_active=True)
    return render(request, 'adminapp/sub_category.html', {'categorys': sub_categorys, 'search': 'page'})

@super_user_required
def add_sub_category(request):
    categories = Category.objects.filter(is_active=True)
    if request.method == 'POST':
        cat = request.POST['subcategory']
        category = Category.objects.get(name=cat)
        SubCategory.objects.create(name=request.POST['category'], Category=category)
    return render(request, 'adminapp/add_sub_category.html', {'categories': categories})

@super_user_required
def edit_sub_category(request, cat_id):
    try:
        category = SubCategory.objects.get(id=cat_id)
        categories = Category.objects.filter(is_active=True)
    except:
        category = None
        categories = None
    if request.method == 'POST':
        category.name=request.POST['category']
        category.save()
        return redirect('sub_category')
    else:
        return render(request, 'adminapp/add_sub_category.html', {'category': category, 'categories': categories})

@super_user_required
def del_sub_category(request, cat_id):
    try:
        category = SubCategory.objects.get(id=cat_id)
        category.is_active = False
        category.save()
    except:
        category = None
    
    return redirect('sub_category')

@super_user_required
def brand(request): 
    brands = Brand.objects.filter(is_active=True)
    return render(request, 'adminapp/brand.html', {'categorys': brands, 'search': 'page'})

@super_user_required
def add_brand(request):
    if request.method == 'POST':
        Brand.objects.create(name=request.POST['category'])
    return render(request, 'adminapp/add_brand.html')

@super_user_required
def edit_brand(request, cat_id):
    try:
        category = Brand.objects.get(id=cat_id)
    except:
        category = None
    if request.method == 'POST':
        category.name=request.POST['category']
        category.save()
        return redirect('brands')
    else:
        return render(request, 'adminapp/add_brand.html', {'category': category, 'search': 'page'})

@super_user_required
def del_brand(request, cat_id):
    try:
        category = Brand.objects.get(id=cat_id)
        category.is_active = False
        category.save()
    except:
        category = None
    
    return redirect('brands')

@super_user_required
def product(request): 
    products = Product.objects.filter(is_active=True).annotate(stock=Sum('variant__stock'))

    if request.method == 'POST':
        searchproduct = True
        data = request.POST['search']
        query = Product.objects.filter(name__icontains=data).annotate(stock=Sum('variant__stock'))
        if query:
            products = query
        else:
            products = 'noproduct'
    else:
        searchproduct = None 

    paginator = Paginator(products, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'products' : products,
        'page_obj': page_obj,
        'search': 'item',
        'searchproduct': searchproduct,
    }
    return render(request, 'adminapp/product.html', context)

@super_user_required
def add_product(request):
    brands = Brand.objects.filter(is_active=True)
    subcategorys = SubCategory.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    colors = COLOR_CHOICES
    sizes = SIZE_CHOICES
    
    context = {
        'brands': brands, 
        'subcategorys': subcategorys, 
        'categories': categories, 
        'colors': colors,
        'sizes': sizes,
        } 
    if request.method == 'POST':
        
        name = request.POST['product-name']
        description = request.POST['desc']
        category = Category.objects.get(name=request.POST['category'])
        subcategory = SubCategory.objects.get(name=request.POST['subcategory'])
        brand = Brand.objects.get(name=request.POST['brand'])
        price = request.POST['price']
        try:
            thump_image = request.FILES['image']
        except:
            messages.error(request, 'Please add image')
            return redirect('add_product')
        
        images = request.FILES.getlist('images')
        color = request.POST.getlist('color')
        print(images, '+++++++++++++++++++======================', color)
        size = request.POST.getlist('size')
        stock = request.POST.getlist('stock')

        product = Product.objects.create(name=name, description=description, category=category,
                                        subcategory=subcategory, brand=brand, price=price, image=thump_image)
        # product.stock = Variant.objects.filter(product=product).aggregate(Sum('stock'))['stock__sum']
        product.save()
        for x in range(len(color)):
            Variant.objects.create(product=product, color=color[x], size=size[x], stock=stock[x])

        for image in images:    
            ProductImage.objects.create(product=product, image=image)
                                         
    return render(request, 'adminapp/add_product.html', context)

@super_user_required
def edit_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        product = None
        
    brands = Brand.objects.filter(is_active=True)
    subcategorys = SubCategory.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    variants = Variant.objects.filter(product=product)
    # colors = Variant.objects.values_list('color', flat=True).distinct()
    # sizes = Variant.objects.values_list('size', flat=True).distinct()
    colors = COLOR_CHOICES
    sizes = SIZE_CHOICES
    images = ProductImage.objects.filter(product=product)

    context = {
            'product': product,
            'variants': variants,
            'brands': brands, 
            'subcategorys': subcategorys, 
            'categories': categories, 
            'colors': colors,
            'sizes': sizes,
            'images': images,
            } 
    if request.method == 'POST':
        
        name = request.POST['product-name']
        description = request.POST.get('desc')
        category = Category.objects.get(name=request.POST['category'])
        subcategory = SubCategory.objects.get(name=request.POST['subcategory'])
        brand = Brand.objects.get(name=request.POST['brand'])
        price = request.POST['price']
        images = request.FILES.getlist('images')
        colors = request.POST.getlist('color')
        print(images, '+++++++++++++++++++======================', colors)
        sizes = request.POST.getlist('size')
        stocks = request.POST.getlist('stock')

        try:
            thump_image = request.FILES['image']
        except:
            thump_image = product.image

        product.name = name
        product.description = description
        product.category = category
        product.subcategory = subcategory
        product.brand = brand
        product.price = price
        product.image = thump_image
        product.save()

        for i in range(len(colors)):
            color = colors[i]
            size = sizes[i]
            stock = stocks[i]
            try:
                variant = Variant.objects.get(product=product, color=color, size=size)
                variant.stock = stock
                variant.save()
            except Variant.DoesNotExist:
                variant = Variant.objects.create(product=product, color=color, size=size, stock=stock)
            except Variant.MultipleObjectsReturned:
                variant = Variant.objects.filter(product=product, color=color, size=size).first()
                variant.stock = stock
                variant.save()

        for image in images:    
            ProductImage.objects.create(product=product, image=image)

        return redirect('products')
    else:
        return render(request, 'adminapp/add_product.html', context)

@super_user_required
def del_image(request, image_id):
    try:
        image = ProductImage.objects.get(id=image_id)
        image.delete()
    except:
        pass

    return redirect('edit_product', image.product.id)

@super_user_required
def del_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.is_active = False
        product.save()
    except:
        product = None
    
    return redirect('products')

@super_user_required   
def del_variant(request, variant_id):
    try:
        variant = Variant.objects.get(id=variant_id)
    except:
        variant = None

    variant.delete()
    return redirect('edit_product', variant.product.id)

@super_user_required   
def admin_order(request):
    orders = Order.objects.all().order_by('-order_no')
    
    paginator = Paginator(orders, 8)
    page_numebr = request.GET.get('page')
    page_obj = paginator.get_page(page_numebr)
    context = {
        'orders' : orders,
        'page_obj': page_obj,
    }
    return render(request, 'adminapp/orderlist.html', context)

@super_user_required
def update_order(request, id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        status = request.POST.get('status')
        if(status):
            order.status = status
            order.save()
        if status  == "Delivered":
            try:
                payment = Payment.objects.get(id = order.payment.id)
                if payment.payment_method == 'cash on delivery':
                    payment.paid = True
                    payment.save()
            except:
                pass
    return redirect('orders')

@super_user_required
def manage_user(request): 
    users = User.objects.filter(is_email_verified=True).order_by('id')

    if request.method == 'POST':
        data = request.POST['search']
        searchuser = User.objects.filter(first_name__icontains=data)
        if searchuser:
            users = searchuser
        else:
            users = 'noproduct'
    else:
        searchuser = None        

    paginator = Paginator(users, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'users' : users,
        'page_obj': page_obj,
        'search': 'item',
        'searchuser': searchuser,
    }
    return render(request, 'adminapp/userlist.html', context)

@super_user_required
def user_action(request, user_id): 
    try:
        user = User.objects.get(id=user_id)
    except:
        user = None

    if user.is_blocked == False:
        user.is_blocked = True
        user.save()
    else:
        user.is_blocked = False
        user.save()

    return redirect('manage_user')

@super_user_required
# @cache_control(no_cache=True,must_revalidate=True,no_store=True)
def view_coupons(request):
    coupons = Coupon.objects.all()
    return render(request,'adminapp/view_coupon.html',{'coupons':coupons})

@super_user_required
def add_coupons(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(view_coupons)
    else:
        form = CouponForm()
    return render(request, 'adminapp/add_coupon.html', {'form': form})

@super_user_required
def edit_coupon(request, pid):
    coupon = Coupon.objects.get(id=pid)

    if request.method == "POST":
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon Updated")
            return redirect(view_coupons)
    else:
        form = CouponForm(instance=coupon)

    return render(request, 'adminapp/edit_coupon.html', {'form': form, 'coupon': coupon})

@super_user_required
def delete_coupon(request, pid):
    coupon = Coupon.objects.get(id=pid)
    coupon.delete()
    messages.success(request, "Coupon Deleted")
    return redirect(view_coupons)


# @super_user_required
# def admin_view_order(request, order_no):
#     try: 
#         order = Order.objects.get(order_no=order_no)
#         order_item = OrderItem.objects.filter(order=order)
#     except:
#         order = None
        
#     context = {'order': order, 'order_items': order_item}    
#     return render(request, 'adminapp/view_order.html', context)

# ##############################################
