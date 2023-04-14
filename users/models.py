from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator

# Create your models here.

STATE_CHOICES = (
    ('Kerala','Kerala'),
    ('Tamilnadu','Tamilnadu'),
    ('Karnataka','Karnataka'),
    ('AndraPradesh','AndraPradesh')
)

DIST_CHOICES = (
    ('Kannur','Kannur'),
    ('Kozhikkode','Kozhikkode'),
    ('Ernakulam','Ernakulam'),
    ('Thiruvananthapuram','Thiruvananthapuram'),
    ('Banglore','Banglore'),
    ('Hubli','Hubli'),
    ('Hydrabad','Hydrabad'),
    ('Coimbator','Coimbator'),
    ('Madurai','Madurai'),
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    image = models.ImageField(upload_to='profile_pic', default='profile_pic/default.jpg')
    is_email_verified = models.BooleanField(default=False)
    mobile_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contains didgits")
    mobile = models.CharField(validators=[mobile_regex], max_length=10, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(unique=True)
    is_blocked = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Address(models.Model):
    first_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile',null=True)
    address = models.TextField(null=True, blank=True)
    district = models.CharField(choices=DIST_CHOICES,max_length=20, null=True, blank=True)
    state = models.CharField(choices=STATE_CHOICES,max_length=20, null=True,blank=True)
    pincode_regex = RegexValidator(regex=r'^\d+$', message="Pincode should only contain digits")
    pincode = models.PositiveIntegerField(null=True, blank=True)
    mobile_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contains didgits")
    mobile = models.CharField(validators=[mobile_regex], max_length=10, null=True, blank=True)

    def str(self):
        return self.user.username