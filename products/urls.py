from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    
    # Authentication URLs
    path("signup/", views.customer_signup, name="customer_signup"),
    path("login/", views.customer_login, name="customer_login"),
    path("logout/", views.customer_logout, name="customer_logout"),
    
    # Admin Dashboard URLs
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/products/", views.admin_products, name="admin_products"),
    path("dashboard/categories/", views.admin_categories, name="admin_categories"),
]