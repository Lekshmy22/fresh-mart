# Generated by Django 5.1.1 on 2024-10-04 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='updated_price',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='ordersummary',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
