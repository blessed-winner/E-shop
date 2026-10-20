from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Category, Product, build_slug

EMOJI_RANGES = [
    (0x1F000, 0x1FAFF),  # pictographs, symbols, supplemental
    (0x2600, 0x27BF),    # misc symbols, dingbats
    (0x2B00, 0x2BFF),    # misc symbols and arrows
    (0xFE0F, 0xFE0F),    # variation selector
    (0x2190, 0x21FF),    # arrows block
    (0x2460, 0x24FF),    # enclosed alphanumerics
    (0x25A0, 0x25FF),    # geometric shapes
]


def find_emojis(text):
    """Return the set of emoji-like characters found in text."""
    return {ch for ch in text if any(lo <= ord(ch) <= hi for lo, hi in EMOJI_RANGES)}


class SlugTests(TestCase):
    def test_default_separator(self):
        self.assertEqual(build_slug("Premium Coffee Beans"), "premium-coffee-beans")

    def test_punctuation_stripped(self):
        self.assertEqual(build_slug("Build & Deploy!"), "build-deploy")

    @override_settings(SLUG_SEPARATOR="_")
    def test_configured_separator_is_used(self):
        self.assertEqual(build_slug("Hello World"), "hello_world")

    @override_settings(SLUG_SEPARATOR="")
    def test_empty_separator_rejected(self):
        with self.assertRaises(ImproperlyConfigured):
            build_slug("Anything")

    @override_settings(SLUG_SEPARATOR="_")
    def test_model_save_uses_configured_separator(self):
        product = Product.objects.create(name="Green Tea Set", price="12.00")
        self.assertEqual(product.slug, "green_tea_set")

    def test_existing_slug_not_regenerated(self):
        category = Category.objects.create(name="Kitchen", slug="custom-slug")
        self.assertEqual(category.slug, "custom-slug")


class StorefrontTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.kitchen = Category.objects.create(name="Kitchen", slug="kitchen")
        cls.audio = Category.objects.create(name="Audio", slug="audio")
        cls.teapot = Product.objects.create(
            name="Cast Iron Teapot", slug="cast-iron-teapot",
            price="48.00", category=cls.kitchen,
            description="A hand-cast teapot that holds heat for hours.",
        )
        cls.mug = Product.objects.create(
            name="Stoneware Mug", slug="stoneware-mug",
            price="14.00", category=cls.kitchen,
        )
        cls.headphones = Product.objects.create(
            name="Studio Headphones", slug="studio-headphones",
            price="199.00", category=cls.audio,
        )
        cls.retired = Product.objects.create(
            name="Retired Lamp", slug="retired-lamp",
            price="90.00", in_stock=False,
        )

    def test_product_list_renders(self):
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cast Iron Teapot")
        self.assertContains(response, "$48.00")
        self.assertContains(response, "site-nav__link--active")

    def test_out_of_stock_products_hidden(self):
        response = self.client.get(reverse("product_list"))
        self.assertNotContains(response, "Retired Lamp")

    def test_category_filter(self):
        response = self.client.get(reverse("product_list"), {"category": "audio"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Studio Headphones")
        self.assertNotContains(response, "Cast Iron Teapot")

    def test_unknown_category_is_404(self):
        response = self.client.get(reverse("product_list"), {"category": "nope"})
        self.assertEqual(response.status_code, 404)

    def test_product_detail_renders(self):
        response = self.client.get(self.teapot.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cast Iron Teapot")
        self.assertContains(response, "cast-iron-teapot")  # SKU from slugify
        self.assertContains(response, "In stock")
        # related items from the same category
        self.assertContains(response, "Stoneware Mug")
        self.assertNotContains(response, "Studio Headphones")

    def test_out_of_stock_detail_is_404(self):
        response = self.client.get(self.retired.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_orders_page_renders(self):
        response = self.client.get(reverse("order_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No orders yet")
        self.assertContains(response, "site-nav__link--active")

    def test_pages_contain_no_emojis(self):
        urls = [
            reverse("product_list"),
            reverse("order_list"),
            self.teapot.get_absolute_url(),
        ]
        for url in urls:
            response = self.client.get(url)
            body = response.content.decode("utf-8")
            self.assertEqual(
                find_emojis(body), set(),
                f"Emoji characters rendered on {url}: {find_emojis(body)}",
            )


class AdminSiteTests(TestCase):
    """Styled admin: login, dashboard and product add/update/delete flows."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.admin = User.objects.create_superuser(
            username="storeadmin",
            email="storeadmin@example.com",
            password="test-pass-123",
        )
        cls.category = Category.objects.create(name="Tools", slug="tools")
        cls.product = Product.objects.create(
            name="Brass Hammer",
            slug="brass-hammer",
            price="25.00",
            description="A balanced brass hammer.",
            category=cls.category,
        )

    def setUp(self):
        self.client.force_login(self.admin)

    def test_login_page_is_styled(self):
        self.client.logout()
        response = self.client.get("/admin/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "products/css/admin.css")
        self.assertContains(response, "Eshop")

    def test_admin_index_renders(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Store administration")
        self.assertContains(response, "products/css/admin.css")

    def test_changelist_renders(self):
        response = self.client.get("/admin/products/product/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brass Hammer")
        self.assertContains(response, 'href="/products/"')  # storefront link

    def test_add_product(self):
        response = self.client.get("/admin/products/product/add/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add product")

        response = self.client.post("/admin/products/product/add/", {
            "name": "Copper Kettle",
            "slug": "copper-kettle",
            "description": "A polished copper kettle.",
            "price": "54.00",
            "category": str(self.category.pk),
            "in_stock": "on",
            "_save": "Save",
        })
        self.assertEqual(response.status_code, 302)
        created = Product.objects.get(slug="copper-kettle")
        self.assertEqual(created.name, "Copper Kettle")
        self.assertEqual(created.category, self.category)

    def test_update_product(self):
        url = f"/admin/products/product/{self.product.pk}/change/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brass Hammer")

        response = self.client.post(url, {
            "name": "Brass Hammer Pro",
            "slug": "brass-hammer",
            "description": "Upgraded brass hammer.",
            "price": "31.50",
            "category": str(self.category.pk),
            "in_stock": "on",
            "_save": "Save",
        })
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Brass Hammer Pro")
        self.assertEqual(str(self.product.price), "31.50")

    def test_delete_product(self):
        confirm_url = f"/admin/products/product/{self.product.pk}/delete/"
        response = self.client.get(confirm_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Are you sure")

        response = self.client.post(confirm_url, {"post": "yes"})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_view_site_link_targets_storefront(self):
        from django.contrib import admin

        self.assertEqual(admin.site.site_url, "/products/")
        self.assertEqual(admin.site.site_header, "Eshop admin")

    def test_admin_pages_contain_no_emojis(self):
        self.client.logout()
        pages = ["/admin/login/"]
        self.client.force_login(self.admin)
        pages += [
            "/admin/",
            "/admin/products/product/",
            "/admin/products/product/add/",
            f"/admin/products/product/{self.product.pk}/change/",
            f"/admin/products/product/{self.product.pk}/delete/",
        ]
        for url in pages:
            response = self.client.get(url)
            body = response.content.decode("utf-8")
            self.assertEqual(
                find_emojis(body), set(),
                f"Emoji characters rendered on {url}: {find_emojis(body)}",
            )
