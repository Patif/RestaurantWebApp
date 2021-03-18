# Generated by Django 3.1.4 on 2021-01-01 09:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('cellphone_number', models.CharField(max_length=12)),
                ('city', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('house_number', models.PositiveSmallIntegerField()),
                ('flat_number', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('zip_code', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(regex='^\\d{2}-\\d{3}$')])),
                ('username_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]