# Generated by Django 3.1.4 on 2021-01-14 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0009_auto_20210110_1341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='weight',
        ),
    ]