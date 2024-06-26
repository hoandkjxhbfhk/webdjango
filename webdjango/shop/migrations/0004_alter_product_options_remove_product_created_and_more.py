# Generated by Django 5.0.3 on 2024-05-06 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_remove_subcategory_category_subcategory_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={},
        ),
        migrations.RemoveField(
            model_name="product",
            name="created",
        ),
        migrations.RemoveField(
            model_name="product",
            name="updated",
        ),
        migrations.AlterField(
            model_name="product",
            name="stock",
            field=models.PositiveIntegerField(default=100),
        ),
    ]
