from django.shortcuts import render,redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import User
from shop.models import Product
from .form import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash

# Email Verification
from .token import *
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.core.mail import send_mail

# Forgot password
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

# Create your views here.

# def home(request):
#     return render(request, 'users/home.html')

class Home(generic.ListView):
    model = Product
    # context_object_name = 'products'
    extra_context = {'title': 'Home'}
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_products = Product.objects.all()[:8]
        context['related_products'] = related_products
        return context

# User login & registration
class UserLoginView(LoginView): 
    template_name = 'users/login.html'
    authentication_form = UserLoginForm
    extra_context ={'title' : 'Login'}
    
    def form_valid(self, form):
        try:
            user = User.objects.get(email=form.cleaned_data.get('username'))
        except(User.DoesNotExist):
            user = None
        if user and user.is_email_verified and not user.is_blocked:
            return super().form_valid(form)
        else:
            form.add_error(None, error='User not verified')
            return super().form_invalid(form) 

class UserRegisterView(generic.CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    message = 'Please check your mail and verify the email'
    extra_context = {'title': 'register', 'message': message}
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Save the user object
        user = form.save(commit=False)

        # Send a verification email to the user
        form.instance.username = form.instance.email
        uid = urlsafe_base64_encode(force_bytes(user.email))

        token_generator = EmailVerificationTokenGenerator()
        token = token_generator.make_token(user)

        verification_link = f"{self.request.scheme}://{self.request.get_host()}{reverse_lazy('verify-email', kwargs={'uidb64': uid, 'token': token})}"
        send_mail(
            subject='Verify your email address',
            message=f'Please click the following link to verify your email address: {verification_link}',
            from_email='your@email.com',
            recipient_list=[user.email],
            fail_silently=False,
        )

        return super().form_valid(form)

class EmailVerificationView(generic.TemplateView):
    template_name = 'users/login.html'
    extra_context ={'title' : 'Login'}
    
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(email=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and email_verification_token.check_token(user, token):
            user.is_email_verified = True
            user.save()

            return redirect('login')
        else:
            return self.render_to_response({'success': False})
        
# Forgot Password---------------->

class PasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = PasswordForgotForm
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class PasswordResetDoneView(generic.TemplateView):
    template_name = 'users/password_reset_form.html'
    extra_context = {'email': 'send'}

class PasswordResetCompleteView(generic.RedirectView):
    url = reverse_lazy('login') 

# User profile
class UserProfileView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "users/profile.html"
    extra_context = {'title': 'user-profile'}

class UserProfileEdit(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'users/profile-edit.html'
    form_class = UserProfileEditForm
    def form_valid(self, form: UserProfileEditForm):
        self.success_url = f'/profile/{self.request.user.id}'
        return super().form_valid(form)
    
class ChangePassword(PasswordChangeView):

    form_class = ChangePasswordForm
    template_name = 'users/change-password.html'
    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data.get('new_password1'))
        self.request.user.save()
        # update_session_auth_hash(self.request,self.request.user)
        return redirect(f'/profile/{self.request.user.id}')

class ManageAddress(generic.ListView):
    model = Address
    template_name = 'users/address.html'
    context_object_name = 'addresses'

    def get_queryset(self):

        self.queryset = Address.objects.filter(user_id = self.request.user.id)
        return super().get_queryset()

class CreateAddressView(generic.CreateView):
    model = Address
    template_name = 'users/edit-address.html'
    form_class = UserAddressForm
    context_object_name = 'addresses'

    def post(self, request, *args: str, **kwargs):
        self.success_url = f'/manage-address/{self.request.user.id}'
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form: UserAddressForm):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required   
def delete_address(request, address_id):

    address = get_object_or_404(Address, id=address_id)
    user = request.user.id
    if request.user.is_authenticated and address.user == request.user:
        address.delete()
    
    return redirect(f'/manage-address/{address_id}')

class EditAddressView(generic.UpdateView):
    model = Address
    template_name = 'users/edit-address.html'
    form_class = UserAddressForm
    context_object_name = 'addresses'

    def post(self, request, *args: str, **kwargs):
        self.success_url = f'/manage-address/{self.request.user.id}'
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form: UserAddressForm):
        form.instance.user = self.request.user
        return super().form_valid(form)



