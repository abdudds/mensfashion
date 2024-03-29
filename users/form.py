from django import forms
from .models import *
from django.contrib.auth import forms as auth_forms, get_user_model
from django.contrib.auth.forms import PasswordChangeForm

class UserLoginForm(auth_forms.AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email','class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control'}))
    # email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})
        self.fields['username'].label = 'Email'
        self.fields['password'].label = 'Password'

    def clean_username(self):
        UserModel = get_user_model()
        
        email = self.cleaned_data.get('username')

        try:
            user = UserModel.objects.get(email=email)
            
        except UserModel.DoesNotExist:
            raise forms.ValidationError("Invalid email or password.")
        return user.username

class UserRegisterForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name','class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name','class': 'form-control'}))
    # username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': 'form-control'}))
   

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

class PasswordForgotForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(max_length=254,widget=forms.EmailInput(attrs={'placeholder': 'Your Email',"autocomplete": "email", 'class': 'form-control-sm'}))

class PasswordSetForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password',"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password',"autocomplete": "new-password", 'class': 'form-control'}),
    )
        
    class Meta:
        model = User
        fields = ('new_password1','new_password2')

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'mobile', 'address', 'image', 'username')
        widgets = {
            'username':forms.TextInput(attrs={'class' : 'form-control'}),
            'address':forms.TextInput(attrs={'class' : 'form-control'}),
            'first_name':forms.TextInput(attrs={'class' : 'form-control'}),
            'last_name':forms.TextInput(attrs={'class' : 'form-control'}),
            'mobile':forms.TextInput(attrs={'class' : 'form-control','minlength': 6, 'maxlength': 6}),
            'image':forms.FileInput(attrs={'class':'form-control-sm ml-5'})
        }

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Old Password',"autocomplete": "new-password", 'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password',"autocomplete": "new-password", 'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password',"autocomplete": "new-password", 'class': 'form-control'}),
    )
        
    class Meta:
        model = User
        fields = ('old_password', 'new_password1','new_password2')

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('first_name', 'mobile', 'address', 'district', 'state', 'pincode')
        widgets = {
            'district':forms.Select(attrs={'class' : 'form-control', 'placeholder': 'District'}),
            'address':forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Address'}),
            'first_name':forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Name'}),
            'state':forms.Select(attrs={'class' : 'form-control', 'placeholder': 'State'}),
            'mobile':forms.TextInput(attrs={'class' : 'form-control','minlength': 6, 'maxlength': 6, 'placeholder': 'Mobile'}),
            'pincode':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Piincode'})
        }