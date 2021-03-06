# Generated by Django 3.1.4 on 2021-01-10 12:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_auto_20210103_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='username_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='client',
            name='zip_code',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(message="Zip code needs to be in format '00-000'", regex='^\\d{2}-\\d{3}$')]),
        ),
    ]
