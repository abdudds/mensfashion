from django.urls import path
from .views import *
# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', AdminLoginView.as_view(), name='adminapp-login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', AdminLogoutView.as_view(), name='admin-logout'),

    # path('sales/', sales, name='sales'),
    path('sales-report/', sales_report, name='sales_report'),


    path('category/', category, name='category'),
    path('add-category/', add_category, name='add-category'),
    path('del-category/<cat_id>', del_category, name='del-category'),
    path('edit-category/<cat_id>', edit_category, name='edit-category'),

    path('sub-category/', sub_category, name='sub_category'),
    path('add-sub-category/', add_sub_category, name='add_sub_category'),
    path('del-sub-category/<cat_id>', del_sub_category, name='del_sub_category'),
    path('edit-sub-category/<cat_id>', edit_sub_category, name='edit_sub_category'),

    path('brands/', brand, name='brands'),
    path('add-brand/', add_brand, name='add_brand'),
    path('del-brand/<cat_id>', del_brand, name='del_brand'),
    path('edit-brand/<cat_id>', edit_brand, name='edit_brand'),

    path('products/', product, name='products'),
    path('add-product/', add_product, name='add_product'),
    path('edit-product/<product_id>', edit_product, name='edit_product'),
    path('del-product/<product_id>', del_product, name='del_product'),
    path('del-variant/<variant_id>', del_variant, name='del_variant'),

    path('orders/', admin_order, name='orders'),
    path('update-order/<id>', update_order, name='update_order'),
    # path('view-order/<order_no>', admin_view_order, name='admin_view_order'),

    path('manage-user/', manage_user, name='manage_user'),
    path('user-block/<user_id>', user_action, name='user_block'),

    path('viewcoupon/', view_coupons, name="viewcoupon"),
    path('addcoupon/', add_coupons, name="addcoupon"),
    path('editcoupon/<int:pid>/', edit_coupon, name="editcoupon"),
    path('deletecoupon/<int:pid>/', delete_coupon, name="deletecoupon")
    
]