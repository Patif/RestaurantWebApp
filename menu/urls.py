from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('<int:foodID>/add', views.add_to_cart, name='add_to_cart'),
    path('<int:foodID>/remove', views.remove_from_cart, name='remove_from_cart'),
    path('<int:foodID>/delete', views.delete_from_cart, name='delete_from_cart'),
    path('summary', views.summary, name='summary'),
    path('delivery', views.delivery_address, name='delivery_address'),
    path('view_orders', views.view_orders, name='view_orders'),
    path('accept_order/<str:orderID>', views.accept_order, name='accept_order'),
    path('finish_order/<str:orderID>', views.finish_order, name='finish_order'),
    path('order', views.order, name='order'),
    path('order/<str:orderID>', views.order_detail, name='order_detail'),
]
