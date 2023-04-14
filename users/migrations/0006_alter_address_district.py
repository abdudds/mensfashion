# Generated by Django 4.1.7 on 2023-03-18 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_address_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='district',
            field=models.CharField(blank=True, choices=[('Kannur', 'Kannur'), ('Kozhikkode', 'Kozhikkode'), ('Madurai', 'Madurai'), ('Hydrabad', 'Hydrabad'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Ernakulam', 'Ernakulam'), ('Hubli', 'Hubli'), ('Coimbator', 'Coimbator'), ('Banglore', 'Banglore')], max_length=20, null=True),
        ),
    ]