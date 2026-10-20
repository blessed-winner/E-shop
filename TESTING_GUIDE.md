# Testing Guide for New Authentication & Admin Dashboard

## Setup Steps

### 1. Start the Development Server

```bash
# Activate virtual environment
.\venv\Scripts\activate.ps1

# Run the server
python manage.py runserver
```

### 2. Create an Admin User (Required for Admin Dashboard)

```bash
# In a new terminal, with venv activated
python manage.py createsuperuser

# Follow the prompts:
# - Username: admin (or your choice)
# - Email: admin@example.com (or your choice)
# - Password: (choose a secure password)
```

## Testing Authentication

### Test Customer Signup
1. Navigate to `http://127.0.0.1:8000/signup/`
2. Fill in the form:
   - First name: John
   - Last name: Doe
   - Username: johndoe
   - Email: john@example.com
   - Password: testpass123
   - Confirm password: testpass123
3. Click "Create account"
4. You should be redirected to the products page
5. Check the header - you should see "Logout" button

### Test Customer Login
1. Log out by clicking "Logout" in the header
2. Navigate to `http://127.0.0.1:8000/login/`
3. Enter credentials:
   - Username: johndoe
   - Password: testpass123
4. Click "Sign in"
5. You should be redirected to the products page with a welcome message

### Test Logout
1. Click "Logout" in the header
2. You should be redirected to the products page
3. Header should now show "Login" and "Sign Up" buttons

## Testing Admin Dashboard

### Access Dashboard (Must be logged in as admin)
1. Log out if logged in as regular customer
2. Navigate to `http://127.0.0.1:8000/login/`
3. Enter admin credentials (from createsuperuser step)
4. After login, you should see "Dashboard" button in header
5. Click "Dashboard" or go to `http://127.0.0.1:8000/dashboard/`

### Test Dashboard Overview
1. You should see:
   - 4 statistics cards (Total Products, In Stock, Out of Stock, Categories)
   - Top Categories table
   - Recent Products table
2. Numbers should reflect your current database

### Test Product Management
1. Click "Products" in the dashboard navigation
2. OR go to `http://127.0.0.1:8000/dashboard/products/`
3. Test features:
   - **Search**: Type a product name in search box, click "Apply"
   - **Category Filter**: Select a category from dropdown, click "Apply"
   - **Stock Filter**: Select "In Stock" or "Out of Stock", click "Apply"
   - **Clear Filters**: Click "Clear" button
   - **Add Product**: Click "Add Product" (takes you to Django admin)
   - **View Product**: Click eye icon to view product in storefront
   - **Edit Product**: Click edit icon to edit in Django admin

### Test Category Management
1. Click "Categories" in the dashboard navigation
2. OR go to `http://127.0.0.1:8000/dashboard/categories/`
3. Test features:
   - **Search**: Type a category name, click "Search"
   - **Clear Search**: Click "Clear" button
   - **Add Category**: Click "Add Category" (takes you to Django admin)
   - **View Products**: Click eye icon to view category products in storefront
   - **Edit Category**: Click edit icon to edit in Django admin

## Expected Behaviors

### Navigation Changes
- **Not logged in**: Header shows "Shop | Orders | Login | Sign Up"
- **Logged in (customer)**: Header shows "Shop | Orders | Logout"
- **Logged in (admin)**: Header shows "Shop | Orders | Dashboard | Logout"

### Access Control
- Regular customers CANNOT access `/dashboard/` URLs
- If they try, they're redirected to login page
- Only users with `is_staff=True` can access dashboard

### Messages
You should see flash messages for:
- ✅ Successful signup: "Welcome to Eshop, [Name]!"
- ✅ Successful login: "Welcome back, [Name]!"
- ℹ️ Logout: "You have been logged out."

## Common Issues & Solutions

### Issue: "Couldn't import Django"
**Solution**: Make sure virtual environment is activated:
```bash
.\venv\Scripts\activate.ps1
```

### Issue: Admin dashboard shows "Permission denied"
**Solution**: User must have staff status. Create superuser or set `is_staff=True` in Django admin.

### Issue: No products/categories showing
**Solution**: Add some test data through Django admin:
1. Go to `http://127.0.0.1:8000/admin/`
2. Add categories
3. Add products

### Issue: CSS not loading
**Solution**: Collect static files or ensure DEBUG=True in settings:
```bash
python manage.py collectstatic
```

## Test Data Setup (Optional)

If you need test data:

```bash
# Django shell
python manage.py shell
```

```python
# In the shell
from products.models import Category, Product

# Create categories
electronics = Category.objects.create(name="Electronics")
clothing = Category.objects.create(name="Clothing")
books = Category.objects.create(name="Books")

# Create products
Product.objects.create(
    name="Laptop",
    description="High-performance laptop",
    price=999.99,
    category=electronics,
    in_stock=True
)

Product.objects.create(
    name="T-Shirt",
    description="Comfortable cotton t-shirt",
    price=19.99,
    category=clothing,
    in_stock=True
)

Product.objects.create(
    name="Python Programming",
    description="Learn Python from scratch",
    price=29.99,
    category=books,
    in_stock=False
)

print("Test data created!")
```

## Screenshots Checklist

Test and verify these pages:
- [ ] Signup page (`/signup/`)
- [ ] Login page (`/login/`)
- [ ] Product list with auth buttons (logged out)
- [ ] Product list with logout button (logged in)
- [ ] Dashboard overview (`/dashboard/`)
- [ ] Product management (`/dashboard/products/`)
- [ ] Category management (`/dashboard/categories/`)
- [ ] Flash messages (success, error, info)

## Next Steps

After testing, you can:
1. Customize the welcome messages
2. Add more statistics to the dashboard
3. Implement password reset
4. Add user profiles
5. Create order management for customers
