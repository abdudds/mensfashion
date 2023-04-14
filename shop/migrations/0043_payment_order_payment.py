# Generated by Django 4.1.7 on 2023-03-29 05:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0042_remove_order_is_coupon_used_alter_order_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razorpay_order_id', models.CharField(blank=True, max_length=30, null=True)),
                ('payment_id', models.CharField(blank=True, max_length=30, null=True)),
                ('refund_id', models.CharField(max_length=30)),
                ('order_id', models.CharField(blank=True, default='empty', max_length=100)),
                ('payment_method', models.CharField(max_length=100)),
                ('amount_paid', models.FloatField(default=0)),
                ('paid', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.payment'),
            preserve_default=False,
        ),
    ]
