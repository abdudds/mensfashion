# Generated by Django 4.1.7 on 2023-03-19 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_address_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='district',
            field=models.CharField(blank=True, choices=[('Banglore', 'Banglore'), ('Ernakulam', 'Ernakulam'), ('Hydrabad', 'Hydrabad'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Hubli', 'Hubli'), ('Madurai', 'Madurai'), ('Coimbator', 'Coimbator'), ('Kozhikkode', 'Kozhikkode'), ('Kannur', 'Kannur')], max_length=20, null=True),
        ),
    ]
