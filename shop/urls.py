from django.urls import path
from .views import *


urlpatterns = [ 
    path('products/', ShopView.as_view(), name='shop'),
    path('search-products/', ShopView.as_view(), name='search-products'),
    path('product/<pk>', ProductView.as_view(), name='product'),

    path('wishlist/', view_wishlist, name='wishlist'),
    path('add-wishlist/<product_id>', add_to_wishlist, name='add_wishlist'),
    path('delete-wishlist/<item_id>', delete_wish_list, name='delete_wishlist'),
    
    path('cart/', view_cart, name='view_cart'),
    path('add-cart/<product_id>', add_to_cart, name='add_cart'),
    path('add-item-cart/<cart_id>', add_item_cart, name='add_item_cart'),
    path('remove-item-cart/<cart_id>', remove_item_cart, name='remove_item_cart'),
    path('delete-cartitem/<item_id>', delete_Cart_Item, name='delete_cartitem'),
   
    path('checkout/', checkout_view, name='checkout'),
    path('applycoupon/<coupon_id>', apply_coupon, name='applycoupon'),
    path('checkout/add-address/pk', CheckoutAddAddressView.as_view(), name='checkout_add_address'),
    path('place-order/', place_order, name='place_order'), 
    path('place-order/paymenthandler/', paymenthandler, name='paymenthandler'),
    path('ordercomplete/<order_no>', order_complete, name='ordercomplete'), 
    path('userorder/', user_order, name='userorder'), 
    path('vieworder/<order_no>', view_order, name='vieworder'), 
    path('cancelorder/<id>', cancelOrder, name='cancelorder'), 

]