from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from .form import *

urlpatterns = [
    path('', Home.as_view(), name='users-home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/<str:uidb64>/<str:token>/', EmailVerificationView.as_view(template_name = 'users/login.html'), name='verify-email'),  
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Forgot password
    path('password_reset/', PasswordResetView.as_view(template_name='users/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_form.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', form_class = PasswordSetForm), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),  

    path('profile/<pk>', UserProfileView.as_view(template_name = "users/profile.html"), name='user-profile'),
    path('profile/edit/<pk>', UserProfileEdit.as_view(template_name = "users/profile-edit.html"), name='user-profile-edit'),
    path('profile/change-password/',ChangePassword.as_view(), name = "user-change-password"),
    path('manage-address/<pk>', ManageAddress.as_view(), name='manage-address'),
    path('add-address/<pk>', CreateAddressView.as_view(), name='add-address'),
    path('delete-address/<address_id>', delete_address, name='delete-address'),
    path('edit-address/<pk>', EditAddressView.as_view(), name='edit-address'),

]