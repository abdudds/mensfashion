# Generated by Django 4.1.7 on 2023-03-23 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0038_order_coupon_order_is_coupon_used_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='max_value',
            field=models.IntegerField(default=1000),
            preserve_default=False,
        ),
    ]
