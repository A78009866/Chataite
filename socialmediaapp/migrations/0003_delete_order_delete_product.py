# Generated by Django 5.1.6 on 2025-03-10 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialmediaapp', '0002_product_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
