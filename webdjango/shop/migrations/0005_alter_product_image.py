# Generated by Django 5.0.3 on 2024-05-06 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_product_options_remove_product_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, max_length=255, upload_to='products/%Y/%m/%d'),
        ),
    ]