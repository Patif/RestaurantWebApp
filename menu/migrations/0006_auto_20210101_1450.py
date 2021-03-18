# Generated by Django 3.1.4 on 2021-01-01 13:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_auto_20210101_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.cart'),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.TimeField(default=datetime.time(13, 50, 29, 572567)),
        ),
    ]