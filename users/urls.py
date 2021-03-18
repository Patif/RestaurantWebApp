from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('edit_data/', views.edit_client, name='edit_client'),
]
