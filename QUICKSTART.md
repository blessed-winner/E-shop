# Quick Start Guide

## Get Started in 3 Steps

### Step 1: Create an Admin User
```bash
# Activate virtual environment
.\venv\Scripts\activate.ps1

# Create superuser
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### Step 2: Start the Server
```bash
# Run development server
python manage.py runserver
```

### Step 3: Visit the Site
Open your browser and visit:
- **Storefront**: http://127.0.0.1:8000/products/
- **Sign Up**: http://127.0.0.1:8000/signup/
- **Login**: http://127.0.0.1:8000/login/
- **Admin Dashboard**: http://127.0.0.1:8000/dashboard/ (after logging in as admin)

## URL Reference

| Page | URL | Access |
|------|-----|--------|
| Products | `/products/` | Public |
| Product Detail | `/products/<slug>/` | Public |
| Sign Up | `/signup/` | Public |
| Login | `/login/` | Public |
| Logout | `/logout/` | Authenticated |
| Dashboard | `/dashboard/` | Staff only |
| Product Management | `/dashboard/products/` | Staff only |
| Category Management | `/dashboard/categories/` | Staff only |
| Django Admin | `/admin/` | Staff only |

## Authentication Flow

### For Customers
1. Click "Sign Up" → Fill form → Auto-login → Shop
2. Or: Click "Login" → Enter credentials → Shop
3. Click "Logout" when done

### For Admins
1. Click "Login" → Enter admin credentials
2. Click "Dashboard" in header
3. Manage products and categories
4. View statistics

## Key Features

✅ **Customer Signup** - New users can create accounts
✅ **Customer Login** - Existing users can sign in
✅ **Session Management** - Stay logged in across pages
✅ **Admin Dashboard** - Statistics and management interface
✅ **Product Management** - Search, filter, view, edit products
✅ **Category Management** - Organize and manage categories
✅ **Secure** - No public admin registration, staff-only access
✅ **Beautiful** - Matches your existing design perfectly

## Need Help?

- **Full Documentation**: See `AUTHENTICATION_README.md`
- **Testing Guide**: See `TESTING_GUIDE.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`

## Common Commands

```bash
# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver

# Check for issues
python manage.py check

# Access Django shell
python manage.py shell

# Make migrations (if needed)
python manage.py makemigrations
python manage.py migrate
```

Enjoy your new authentication system and admin dashboard! 🎉
