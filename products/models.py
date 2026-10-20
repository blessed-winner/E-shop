from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.urls import reverse
from slugify_plus import slugify


def build_slug(text):
    """Slugify ``text`` with the separator configured in SLUG_SEPARATOR.

    slugify-plus validates its inputs (TypeError for non-strings, ValueError
    for an empty separator); a bad setting is surfaced as ImproperlyConfigured
    so misconfiguration is caught early instead of failing at runtime.
    """
    separator = getattr(settings, "SLUG_SEPARATOR", "-")
    if not isinstance(separator, str) or not separator:
        raise ImproperlyConfigured(
            "SLUG_SEPARATOR must be a non-empty string (requirement of "
            "slugify-plus)."
        )
    return slugify(text, separator=separator)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, max_length=120)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = build_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=280)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = build_slug(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name
