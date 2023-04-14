# Generated by Django 4.1.7 on 2023-03-18 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_address_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='district',
            field=models.CharField(blank=True, choices=[('Hubli', 'Hubli'), ('Kannur', 'Kannur'), ('Hydrabad', 'Hydrabad'), ('Ernakulam', 'Ernakulam'), ('Coimbator', 'Coimbator'), ('Kozhikkode', 'Kozhikkode'), ('Madurai', 'Madurai'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Banglore', 'Banglore')], max_length=20, null=True),
        ),
    ]
