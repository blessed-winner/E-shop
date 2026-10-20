from .views import say_hello
from .views import order_list
from django.urls import path

urlpatterns = [
    path('hello/', say_hello, name='say_hello'),
    path('orders/', order_list, name='order_list')
]