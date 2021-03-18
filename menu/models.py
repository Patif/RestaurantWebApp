from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator
from users.models import Client
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
import os


class Food(models.Model):
    name = models.CharField(max_length=30)
    photo = models.FilePathField(path="{}\\menu\\static\\food".format(os.getcwd()), blank=True)
    in_offer = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(default=Decimal(0), max_digits=5, decimal_places=2,
                                validators=[MinValueValidator(Decimal(0))])

    def __str__(self):
        return self.name

    @property
    def get_file(self):
        return "food/{}".format(os.path.basename(self.photo))

    class Meta:
        verbose_name_plural = 'Food'


class Order(models.Model):
    number = models.PositiveBigIntegerField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.RESTRICT)
    date = models.DateField()
    time = models.TimeField()
    accepted = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    @property
    def sum_order(self):
        sum = 0
        for item in self.cartitem_set.all():
            sum += item.price()
        return sum

    def __str__(self):
        return "{} {}".format(self.number, str(self.client))


class Cart(models.Model):
    session_id = models.OneToOneField(Session, on_delete=models.CASCADE, primary_key=True)
    order_id = models.OneToOneField(Order, on_delete=models.RESTRICT, blank=True, null=True)

    def sum_cart(self):
        sum = 0
        for item in self.cartitem_set.all():
            sum += item.price()
        return sum

    def __str__(self):
        content = [str(self.pk), ": "]
        for item in self.cartitem_set.all():
            content.append(str(item))
            content.append(" ")
        return "".join(content)


class CartItem(models.Model):
    cart_number = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    order_number = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return "{} x{}".format(self.food_id, self.quantity)

    def price(self):
        return self.food_id.price * self.quantity
