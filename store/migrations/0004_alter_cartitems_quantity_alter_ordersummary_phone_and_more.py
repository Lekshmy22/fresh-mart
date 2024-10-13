# Generated by Django 5.1.1 on 2024-10-04 15:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_category_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='quantity',
            field=models.PositiveIntegerField(default=1, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)]),
        ),
        migrations.AlterField(
            model_name='ordersummary',
            name='phone',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='rating',
            field=models.PositiveIntegerField(default=1, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
