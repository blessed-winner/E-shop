from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from .models import Product, Category
from .forms import CustomerSignupForm, CustomerLoginForm


def product_list(request):
    """Show all in-stock products, optionally filtered by category slug."""
    categories = Category.objects.all()
    category_slug = request.GET.get("category")
    active_category = None

    products = Product.objects.filter(in_stock=True)
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)

    return render(request, "products/product_list.html", {
        "products": products,
        "categories": categories,
        "active_category": active_category,
        "active_page": "shop",
    })


def product_detail(request, slug):
    """Show a single product page identified by its slug."""
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    related = Product.objects.filter(
        category=product.category, in_stock=True
    ).exclude(pk=product.pk)[:4]

    return render(request, "products/product_detail.html", {
        "product": product,
        "related": related,
        "active_page": "shop",
    })


# ==================== Authentication Views ====================

def customer_signup(request):
    """Customer registration view."""
    if request.user.is_authenticated:
        return redirect('product_list')
    
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Eshop, {user.first_name}!')
            return redirect('product_list')
    else:
        form = CustomerSignupForm()
    
    return render(request, 'products/signup.html', {
        'form': form,
        'active_page': 'signup'
    })


def customer_login(request):
    """Customer login view."""
    if request.user.is_authenticated:
        return redirect('product_list')
    
    if request.method == 'POST':
        form = CustomerLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_url = request.GET.get('next', 'product_list')
                return redirect(next_url)
    else:
        form = CustomerLoginForm()
    
    return render(request, 'products/login.html', {
        'form': form,
        'active_page': 'login'
    })


def customer_logout(request):
    """Customer logout view."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('product_list')


# ==================== Admin Dashboard Views ====================

def is_staff_user(user):
    """Check if user is staff (admin)."""
    return user.is_staff


@login_required
@user_passes_test(is_staff_user)
def admin_dashboard(request):
    """Admin dashboard with statistics."""
    total_products = Product.objects.count()
    in_stock_products = Product.objects.filter(in_stock=True).count()
    out_of_stock = total_products - in_stock_products
    total_categories = Category.objects.count()
    
    # Category stats
    categories_with_counts = Category.objects.annotate(
        product_count=Count('products')
    ).order_by('-product_count')[:5]
    
    # Recent products
    recent_products = Product.objects.all()[:10]
    
    context = {
        'active_page': 'admin_dashboard',
        'total_products': total_products,
        'in_stock_products': in_stock_products,
        'out_of_stock': out_of_stock,
        'total_categories': total_categories,
        'categories_with_counts': categories_with_counts,
        'recent_products': recent_products,
    }
    
    return render(request, 'products/admin_dashboard.html', context)


@login_required
@user_passes_test(is_staff_user)
def admin_products(request):
    """Admin product management view."""
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    stock_filter = request.GET.get('stock', '')
    
    products = Product.objects.all()
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(slug__icontains=search_query)
        )
    
    if category_filter:
        products = products.filter(category__slug=category_filter)
    
    if stock_filter == 'in_stock':
        products = products.filter(in_stock=True)
    elif stock_filter == 'out_of_stock':
        products = products.filter(in_stock=False)
    
    categories = Category.objects.all()
    
    context = {
        'active_page': 'admin_dashboard',
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'stock_filter': stock_filter,
    }
    
    return render(request, 'products/admin_products.html', context)


@login_required
@user_passes_test(is_staff_user)
def admin_categories(request):
    """Admin category management view."""
    search_query = request.GET.get('q', '')
    
    categories = Category.objects.annotate(
        product_count=Count('products')
    )
    
    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query) | Q(slug__icontains=search_query)
        )
    
    context = {
        'active_page': 'admin_dashboard',
        'categories': categories,
        'search_query': search_query,
    }
    
    return render(request, 'products/admin_categories.html', context)
