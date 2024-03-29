# Generated by Django 4.1.7 on 2023-03-16 20:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('address', models.TextField(blank=True, null=True)),
                ('district', models.CharField(blank=True, choices=[('Ernakulam', 'Ernakulam'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Kannur', 'Kannur'), ('Kozhikkode', 'Kozhikkode'), ('Coimbator', 'Coimbator'), ('Banglore', 'Banglore'), ('Madurai', 'Madurai'), ('Hubli', 'Hubli'), ('Hydrabad', 'Hydrabad')], max_length=20, null=True)),
                ('state', models.CharField(blank=True, choices=[('Kerala', 'Kerala'), ('Tamilnadu', 'Tamilnadu'), ('Karnataka', 'Karnataka'), ('AndraPradesh', 'AndraPradesh')], max_length=20, null=True)),
                ('pincode', models.PositiveIntegerField(blank=True, null=True)),
                ('mobile', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='Mobile number should only contains didgits', regex='^\\d+$')])),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
