# Generated by Django 3.1.4 on 2021-01-01 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='session_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='sessions.session'),
        ),
    ]
