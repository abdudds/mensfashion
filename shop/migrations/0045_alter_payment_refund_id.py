# Generated by Django 4.1.7 on 2023-03-29 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0044_alter_order_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='refund_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]