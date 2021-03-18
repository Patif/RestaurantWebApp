from django.shortcuts import render, redirect, get_object_or_404
from .models import Food, Cart, Order
from users.models import Client
from Projekt.settings import CURRENCY
from django.utils.timezone import now
from .synchronize import synchronized
from users.forms import EditClientData
from home.constants import RESTAURANT_GROUP


def get_cart(session):
    if not session.session_key:
        session.save()
    try:
        cart = Cart.objects.get(pk=session.session_key)
    except Cart.DoesNotExist:
        cart = Cart(pk=session.session_key)
        cart.save()
    return cart


def menu(request):
    cart = get_cart(request.session)
    message = request.session.get('message', None)
    if request.session.get('order_id', None):
        request.session['order_id'] = None
    request.session['message'] = None
    return render(request, 'menu/menu.html', {'food': Food.objects.filter(in_offer=True), 'currency': CURRENCY,
                                              'cart': cart.cartitem_set.all(), 'cost': cart.sum_cart(),
                                              'message': message})


def add_to_cart(request, foodID):
    cart = get_cart(request.session)
    dish = get_object_or_404(Food, pk=foodID)
    queryset = cart.cartitem_set.filter(food_id=foodID)
    if not queryset:
        cart.cartitem_set.create(cart_number=cart, food_id=dish).save()
        message = "Item added to cart."
    else:
        queryset[0].quantity += 1
        queryset[0].save()
        message = "Quantity increased."
    request.session['message'] = message
    return redirect('menu')


def remove_from_cart(request, foodID):
    cart = get_cart(request.session)
    queryset = cart.cartitem_set.filter(food_id=foodID)
    if not queryset:
        request.session['message'] = "No such position in the cart."
        return redirect('menu')
    else:
        queryset[0].quantity -= 1
        if queryset[0].quantity == 0:
            return delete_from_cart(request, foodID, queryset[0])
        queryset[0].save()
    request.session['message'] = "Quantity decreased."
    return redirect('menu')


def delete_from_cart(request, foodID, food=None):
    if not food:
        cart = get_cart(request.session)
        queryset = cart.cartitem_set.filter(food_id=foodID)
        if not queryset:
            request.session['message'] = "No such position in the cart."
            return redirect('menu')
        food = queryset[0]
    food.delete()
    request.session['message'] = "Item removed from cart."
    return redirect('menu')


def delivery_address(request):
    cart = get_cart(request.session)
    if not cart.cartitem_set.all():
        return redirect('menu')
    client = None
    if request.user.is_authenticated:
        client = Client.objects.filter(username_id=request.user)
    if request.method == "GET":
        form = EditClientData(instance=client[0] if client else None)
        return render(request, 'menu/delivery_address.html', {"form": form})
    elif request.method == "POST":
        form = EditClientData(request.POST, instance=client[0] if client else None)
        if form.is_valid():
            if client:
                if form.has_changed():
                    form = EditClientData(request.POST)
            client = form.save()
            request.session['client_id'] = client.pk
            if request.user.is_authenticated and request.user.client is None:
                request.user.client = client
                client.save()
            return redirect('summary')
        return render(request, 'menu/delivery_address.html', {"form": form})


def summary(request):
    cart = get_cart(request.session)
    if not cart.cartitem_set.all():
        return redirect('menu')
    return render(request, 'menu/summary.html', context={'currency': CURRENCY, 'cart': cart.cartitem_set.all(),
                                                         'cost': cart.sum_cart()})


def order(request):
    cart = get_cart(request.session)
    if not cart.cartitem_set.all():
        return redirect('menu')
    client_id = request.session.get('client_id', None)
    if not client_id:
        return redirect('delivery_address')
    order = add_order(client_id, request.user if request.user.is_authenticated else None)
    for cart_item in cart.cartitem_set.all():
        cart.cartitem_set.remove(cart_item)
        order.cartitem_set.add(cart_item)
    cart.delete()
    return redirect('order_detail', orderID=order.pk)


@synchronized
def add_order(client_id, user=None):
    timestamp = now()
    month = timestamp.month
    if month < 10:
        month = "0{}".format(month)
    day = timestamp.day
    if day < 10:
        day = "0{}".format(day)
    number = len(Order.objects.filter(date=timestamp.date())) + 1
    while len(str(number)) < 4:
        number = "0{}".format(number)
    order_number = "{}{}{}{}".format(timestamp.year, month, day, number)
    order = Order(number=order_number, client=Client.objects.get(pk=client_id), date=timestamp.date(),
                  time=timestamp.time(), user=user)
    order.save()
    return order


def order_detail(request, orderID):
    client = request.session.get('client_id', None)
    order = get_object_or_404(Order, pk=orderID)
    if not client or order.client != Client.objects.get(pk=client):
        return redirect('home')
    return render(request, 'order/order_detail.html', context={'order_id': orderID,
                                                               'content': order.cartitem_set.all(),
                                                               'currency': CURRENCY,
                                                               'cost': order.sum_order,
                                                               'accepted': order.accepted,
                                                               'finished': order.finished})


def view_orders(request):
    if not request.user.is_authenticated:
        return redirect('home')
    is_restaurant = request.user.groups.filter(name=RESTAURANT_GROUP).exists()
    if is_restaurant:
        orders = Order.objects.filter(finished=False)
    else:
        orders = Order.objects.filter(user=request.user)
    message = request.session.get('message', None)
    request.session['message'] = None
    return render(request, 'order/view_orders.html', context={
        'orders': orders, 'message': message, 'is_restaurant': is_restaurant, 'currency': CURRENCY,})


def accept_order(request, orderID):
    if not request.user.groups.filter(name=RESTAURANT_GROUP).exists():
        return redirect('home')
    order = get_object_or_404(Order, pk=orderID)
    order.accepted = True
    order.save()
    request.session['message'] = "Order number {} was accepted".format(orderID)
    return redirect('view_orders')


def finish_order(request, orderID):
    if not request.user.groups.filter(name=RESTAURANT_GROUP).exists():
        return redirect('home')
    order = get_object_or_404(Order, pk=orderID)
    order.finished = True
    order.save()
    request.session['message'] = "Order number {} was finished".format(orderID)
    return redirect('view_orders')
