# Generated by Django 4.1.7 on 2023-03-22 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_order_order_no_alter_order_delivery_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_expected_date',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='order_total',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='total_price',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_no',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Order Confirmed', 'Order Confirmed'), ('Shipped', 'Shipped'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], default='Order Confirmed', max_length=50),
        ),
    ]
