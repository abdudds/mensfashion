# Generated by Django 4.1.7 on 2023-03-19 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_address_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='district',
            field=models.CharField(blank=True, choices=[('Kannur', 'Kannur'), ('Kozhikkode', 'Kozhikkode'), ('Ernakulam', 'Ernakulam'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Banglore', 'Banglore'), ('Hubli', 'Hubli'), ('Hydrabad', 'Hydrabad'), ('Coimbator', 'Coimbator'), ('Madurai', 'Madurai')], max_length=20, null=True),
        ),
    ]