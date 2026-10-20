from django.shortcuts import render
from django.http import HttpResponse


def say_hello(request):
    return HttpResponse("Hello, World!")


def order_list(request):
    """Show the customer's orders page (empty until order models exist)."""
    return render(request, "orders/order_list.html", {"active_page": "orders"})
