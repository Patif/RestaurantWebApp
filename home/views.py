from django.shortcuts import render
from .constants import RESTAURANT_GROUP


def home(request):
    message = request.session.get('message', None)
    request.session['message'] = None
    return render(request, 'home/home.html', {'is_restaurant': request.user.groups.filter(name=RESTAURANT_GROUP).exists(
    ), 'message': message})


def about(request):
    return render(request, 'about/about.html')
