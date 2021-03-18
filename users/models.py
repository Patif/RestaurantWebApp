from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.timezone import now


class Client(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    cellphone_number = models.CharField(max_length=12)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.PositiveSmallIntegerField()
    flat_number = models.PositiveSmallIntegerField(blank=True, null=True)
    zip_code = models.CharField(max_length=6, validators=[
        RegexValidator(regex="^\d{2}-\d{3}$", message="Zip code needs to be in format '00-000'")])
    username_id = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    create_date = models.DateField(default=now().date())

    def __str__(self):
        return "{} {} {}".format(self.pk, self.name, self.surname)
