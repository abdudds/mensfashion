from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.form import UserAddressForm
from .models import *
from users.models import Address
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg
from django.contrib import messages
from django.http import JsonResponse


#Razorpay
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.core.mail import send_mail


# Create your views here.
class ShopView(ListView):
    model = Product
    context_object_name = 'products'
    brands = Brand.objects.all().order_by('name')
    categorys = Category.objects.all()
    # products = Product.objects.filter(is_active=True).annotate(stock=Sum('variant__stock'))
    extra_context = {'brands': brands, 'categorys': categorys, 'title': 'shop'}
    template_name = 'shop/shop.html'

    paginate_by = 9

    def post(self, request):
        data = request.POST['search']
        categorys = Category.objects.all()
        brands = Brand.objects.all().order_by('name')
        searchproduct = Product.objects.filter(name__icontains=data)
        if searchproduct:
            self.extra_context = {'searchproduct' : searchproduct, 'brands': brands, 'categorys': categorys,} 
        else:
            self.extra_context = {'searchproduct' : 'noproduct'} 
        return self.get(request)

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('filterbycategory')
        brand = self.request.GET.get('filterbybrand')
        lowtohigh = self.request.GET.get('lowtohigh')
        hightolow = self.request.GET.get('hightolow')
        if category:
            queryset = queryset.filter(category__name__iexact=category).order_by()
        if brand:
            queryset = queryset.filter(brand__name__iexact=brand).order_by()
        if lowtohigh:
            queryset = queryset.all().order_by('price')
        if hightolow:
            queryset = queryset.all().order_by('-price')
            
        return queryset
        

class ProductView(DetailView):
    model = Product
    context_object_name = 'product'
    extra_context = {'title': 'shop'}
    template_name = 'shop/shop-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = ProductImage.objects.filter(product = self.object)[:4]
        variants = Variant.objects.filter(product = self.object)
        total_stock = variants.aggregate(Sum('stock'))['stock__sum']

        colors = set()
        for variant in variants:
            colors.add(variant.color)
        sizes = set()
        for variant in variants:
            sizes.add(variant.size)
        
        related_products = Product.objects.filter(category = self.object.category).exclude(id = self.object.id)[:4]
        context['related_products'] = related_products
        context['images'] = images
        context['colors'] = colors
        context['sizes'] = sizes
        context['total_stock'] = total_stock
        reviews = Review.objects.filter(product = self.object)
        context['reviews'] = reviews

           
        try:
            avg_rating = round(reviews.aggregate(Avg('rating'))['rating__avg'], 1)
        except:
            avg_rating = 0
        context['avg_rating'] = avg_rating
        return context
    
    def post(self, request, *args, **kwargs):
        
        try:
            orders = Order.objects.filter(user=self.request.user)
            product = OrderItem.objects.filter(order__user = self.request.user, variant__product__id = kwargs['pk'])
            
        except:
            orders = None
            product = None 
            messages.error(request, "You cannot rate this product as you haven't purchased this product")

        if product:
            try:
                rating = request.POST['rating']
                review_body = request.POST['review-body']
                title = request.POST['review-title']
            except:
                rating = None
                review_body = None
                title = None
            if rating == 'None':
                return redirect('product')    
            product = Product.objects.get(id=kwargs['pk'])
            print(request.user)
            Review.objects.create(user=request.user, product=product, rating = rating, user_review = review_body, title = title)

            return self.get(request)
        else:
            messages.error(request, "You cannot rate this product as you haven't purchased this product")
            return self.get(request)

#---- WISHLIST ----#

def view_wishlist(request):
    if request.user.is_authenticated:
        user = request.user
        wish_list = WishList.objects.filter(user=user).order_by('id')

    else:
        cart = request.session.get('cart', {})
        wish_list = []
        for product_id in cart.items():
            product = Product.objects.get(id=product_id)
            wish_list.append({
                'product': product,
            })

    return render(request, 'shop/wishlist.html', {'wish_list': wish_list})

def add_to_wishlist(request, product_id):

    try:
        product = Product.objects.get(id=product_id)
    except:
        product = None
        messages.error(request, 'Product not found')
        return redirect('shop')

    if request.user.is_authenticated:
        user = request.user
        wish_list, created = WishList.objects.get_or_create(user=user, product=product)
        wish_list.save()
        messages.success(request, 'Item added to wishlist')
    
    return redirect('shop')

def delete_wish_list(request, item_id):

    try:
        item = WishList.objects.get(id=item_id)
    except:
        item = None
        messages.error(request, 'Product not deleted')
        return redirect('wishlist')

    if request.user.is_authenticated:
        if item.user != request.user:
            return redirect('wishlist')

    if request.user.is_authenticated and item.user == request.user:
        item.delete()
        messages.success(request, 'Item removed from wishlist')

    return redirect('wishlist') 

#---- Cart View ----#
@login_required
def view_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart_items = CartItem.objects.filter(user=user).order_by('id')
        total = cart_items.aggregate(Sum('total_price'))['total_price__sum']

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})  

@login_required
def add_to_cart(request, product_id):

    try:
        color = request.POST['color']
        size = request.POST['size']
    except:
        color = None
        size = None
        messages.info(request, 'Please select the size and color!')
        return redirect(f'/shop/product/{product_id}')     

    try:
        product = Product.objects.get(id=product_id)
    except:
        product = None
        messages.error(request, 'Product not found')
        return redirect('product')
    
    try:
        variant = Variant.objects.get(product=product_id, color = color, size = size)
    except:
        variant = None
    quantityk = request.POST.get('quantity', 1)

    if request.user.is_authenticated:
        user = request.user
        if variant:
            cart_item, created = CartItem.objects.get_or_create(user=user, product=product, variant= variant)
            if variant.stock <= cart_item.quantity:
                cart_item.quantity = variant.stock
            else:
                cart_item.quantity += int(quantityk)
            cart_item.total_price = cart_item.quantity*product.price
            cart_item.save()

        else:
            messages.success(request, 'Selected variant out of stock. Please choose other variant')
            return redirect(f'/shop/product/{product_id}')

    return redirect('view_cart')

def add_item_cart(request, cart_id):

    item = CartItem.objects.get(id = cart_id)
    if request.user.is_authenticated:
        if item.variant.stock <= item.quantity:
            item.quantity = item.variant.stock
        else:
            item.quantity += 1
        item.total_price = item.quantity*item.product.price
        item.save()
    return redirect('view_cart')

def remove_item_cart(request, cart_id):

    try:
        item = CartItem.objects.get(id = cart_id)
    except:
        item = None
        messages.error(request, 'item not found')
        return redirect('view_cart')
        
    if request.user.is_authenticated:
        if item.variant.stock == 0:
            item.quantity = item.variant.stock
        elif item.quantity == 0:
            item.quantity = 0
        else:
            item.quantity -= 1
        item.total_price = item.quantity*item.product.price
        item.save()
    return redirect('view_cart')

def delete_Cart_Item(request, item_id):

    item = get_object_or_404(CartItem, id=item_id)

    if request.user.is_authenticated:
        if item.user != request.user:
            return redirect('view_cart')

    if request.user.is_authenticated and item.user == request.user:
        item.delete()

    return redirect('view_cart')

# Checkout View

@login_required
def checkout_view(request,**kwargs):    
    discount = 0
    if kwargs:
        discount = kwargs['discount_amount']

    addresses = Address.objects.filter(user = request.user)
    cart_item = CartItem.objects.filter(user =request.user)
    coupons = Coupon.objects.filter()

    if not cart_item:
        msg = 'Please add items to cart'
        return redirect('shop')

    total = cart_item.aggregate(Sum('total_price'))['total_price__sum']
    sub_total = total - discount
    context = {'addresses': addresses, 'cart_item': cart_item, 'total': total, 'coupons': coupons,'discount':discount,'sub_total':sub_total}

    return render(request, 'shop/checkout.html', locals())

@login_required
def apply_coupon(request, coupon_id):
    
    try:
        coupon = Coupon.objects.get(id=coupon_id)
    except:
        coupon = None
        return redirect('checkout')
    
    cart_items = CartItem.objects.filter(user=request.user)  
    cart_total = cart_items.aggregate(Sum('total_price'))['total_price__sum']
    forder = Order.objects.filter(user=request.user)
    
    discount = 0
    msg = None
    if coupon:
        coupon_not_used = True
        for order in forder:
            if order.coupon==coupon:
              
                coupon_not_used = False
                msg = 'Coupon already applied'
                break  
        
        if coupon.active and coupon_not_used:
            if cart_total >= coupon.min_value:
                discount = coupon.discount*cart_total/100
                if discount >= coupon.max_value:
                    discount = coupon.max_value
            else:
                discount = 0
                msg = 'Coupon not applicable'
    

    return JsonResponse({'discount':discount,'message':msg})

class CheckoutAddAddressView(LoginRequiredMixin, CreateView):
    model = Address
    template_name = 'shop/edit-address.html'
    form_class = UserAddressForm
    context_object_name = 'addresses'

    def post(self, request, *args: str, **kwargs):
        self.success_url = '/shop/checkout/'
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form: UserAddressForm):
        form.instance.user = self.request.user
        return super().form_valid(form)

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


@login_required
def place_order(request):
    
    try:
        address_id = request.POST['address']
        address = Address.objects.get(id=address_id)
        payment_method = request.POST['payment']
    except:
        address_id = None
        address = None
        payment = None
        return redirect('checkout')

    try: 
        coupon_id = request.POST['coupon']
        coupon = Coupon.objects.get(id=coupon_id)
    except:
        coupon_id = None
        coupon = None

    cart_items = CartItem.objects.filter(user=request.user)
    order_total = cart_items.aggregate(Sum('total_price'))['total_price__sum']
    forder = Order.objects.filter(user=request.user)
    
    discount = 0
    if coupon_id:
        coupon_not_used = True
        for order in forder:
            if order.coupon==coupon:
                coupon_not_used = False
                break    
        if coupon.active & coupon_not_used:
            if order_total >= coupon.min_value:
                discount = round(coupon.discount*order_total/100, 2)
                if discount >= coupon.max_value:
                    discount = coupon.max_value
            else:
                discount = 0
        else:
            discount = 0

    total = order_total - discount

    try:
        sorder = Order.objects.all().order_by('-order_no').first()
        order_no = sorder.order_no; 
    except:
        order_no = 215716

    order = Order.objects.create(user=request.user, delivery_address=address, order_no = order_no+1, order_total = order_total)
    if discount:
        order.discount = discount
        order.coupon = coupon
    order.save()    

    for cart_item in cart_items:
        quantity = cart_item.quantity
        total_price = cart_item.total_price
        variant = cart_item.variant
        variant.stock -= quantity
        variant.save()
        OrderItem.objects.get_or_create(order=order, quantity=quantity, total_price=total_price, variant=variant)

    payment = Payment.objects.create(user=request.user)
    payment.order_id = order.order_no
    payment.amount_paid = total
    payment.save()

    if payment_method == 'razorpay':
        currency = 'INR'
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=int(total*100),currency=currency,payment_capture='0'))

    # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        payment.razorpay_order_id = razorpay_order_id
        payment.payment_method = 'razorpay'
        payment.save()
        order.payment = payment
        order.save()
        callback_url = 'paymenthandler/'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = total
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['order_no'] = order_no
        context['cart_items'] = cart_items
        context['discount'] = discount
        context['order_total'] = order_total
        context['address_id'] = address_id
        context['coupon_id'] = coupon_id

        return render(request, 'shop/payment.html', context=context)

    else:
        payment.payment_method = 'cash on delivery'
        payment.save()
        order.payment = payment
        order.save()
        order_item = OrderItem.objects.filter(order=order)
        
        cart_items.delete()

        return redirect('ordercomplete', order.order_no)


@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.payment_id = payment_id
            payment.paid = True
            payment.save()
            cart_items = CartItem.objects.filter(user=payment.user)
            cart_items.delete()
            order = Order.objects.get(payment=payment.id)
            order_no = order.order_no
            print(order_no, '\n\n\n')
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            
            if result is not None:
                amount = int(payment.amount_paid*100)
                try:
                    
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    
                    # render success page on successful caputre of payment
                    return redirect('ordercomplete', order_no)
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

@login_required
def order_complete(request, order_no):
    try: 
        order = Order.objects.get(order_no=order_no)
        order_item = OrderItem.objects.filter(order=order)

    except:
        order = None
        
    context = {'order': order, 'order_items': order_item}    
    return render(request, 'shop/paymentsuccess.html', context)

@login_required    
def user_order(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_no')
    
    return render(request, 'shop/user_order.html', {'orders': orders})   


@login_required
def view_order(request, order_no):
    try: 
        order = Order.objects.get(order_no=order_no)
        order_item = OrderItem.objects.filter(order=order)
    except:
        order = None
        
    context = {'order': order, 'order_items': order_item}    
    return render(request, 'shop/vieworder.html', context)

def cancelOrder(request, id):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    client = razorpay.Client(auth=("rzp_test_a08czAcvdoxBL5", "gpesereRmTOMwbSbmgP80KrY"))
    order = Order.objects.get(id=id, user=request.user)
    payment = order.payment
    msg = ''

    if payment.payment_method == 'razorpay':
        payment_id = payment.payment_id
        print(payment_id)
        amount = payment.amount_paid
        amount = int(amount * 100)
        print(amount)
        print('###########')
        
        if payment.paid:
            refund_data = {
                "payment_id": payment_id,
                "amount": amount,  # amount to be refunded in paise
                "currency": "INR",
            }
        else:
            msg = "Your bank has not completed the payment yet."
            messages.error(request, msg)
            orderitems = OrderItem.objects.filter(order=order)
            context = {
                'order': order,
                'orderitems': orderitems,
                'msg': msg
            }
            return render(request, 'shop/vieworder.html', context)

        refund = client.payment.refund(payment_id, refund_data)
        print(refund)

        if refund is not None:
            current_user = request.user
            order.refund_completed = True
            order.status = 'Cancelled'
            payment = order.payment
            payment.refund_id = refund['id']
            payment.save()
            order.save()
            msg = "Your order has been successfully cancelled and amount has been refunded!"
            mess = f'Hello\t{current_user.first_name},\nYour order has been canceled,Money will be refunded with in 1 hour\nThanks!'
            send_mail(
                "MensFashion  - Order Cancelled",
                mess,
                settings.EMAIL_HOST_USER,
                [current_user.username],
                fail_silently=False
            )
            messages.success(request, msg)
        else:
            msg = "Your order is not cancelled because the refund could not be completed now. Please try again later. If the issue continues, CONTACT THE SUPPORT TEAM!"
            messages.error(request, msg)
            pass
    else:
        if payment.paid:
            order.refund_completed = True
            order.status = 'Cancelled'
            msg = "YOUR ORDER HAS BEEN SUCCESSFULLY CANCELLED!"
            order.save()
            messages.success(request, msg)
        else:
            order.status = 'Cancelled'
            order.save()
            msg = "Your payment has not been received yet. But the order has been cancelled."
            messages.warning(request, msg)

    orderitems = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'orderitems': orderitems,
        'msg': msg,
        'title':'refunded'
    }
    return render(request, 'shop/vieworder.html',context)