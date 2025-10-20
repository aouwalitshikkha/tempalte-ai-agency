from django.db import models
from django.utils.text import slugify

class Service(models.Model):
    service_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.TextField(
        max_length=300,
        help_text="A short description to display on the homepage."
    )
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-code",
        help_text="FontAwesome icon class (e.g., 'fa-solid fa-robot')."
    )

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ["service_name"]

    def __str__(self):
        return self.service_name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.service_name)
            slug = base_slug
            counter = 1
            while Service.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)




class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    company = models.CharField(max_length=200, blank=True, null=True)

    # Optional — only used when submitted from home page
    service_interested = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contacts',
        help_text="Selected service if submitted from homepage."
    )

    # Automatically captured when submitted from subservice or other pages
    page_source = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Readable page or section name where the form was submitted (e.g. 'SEO Automation')."
    )

    page_url = models.URLField(
        blank=True,
        null=True,
        help_text="Full URL of the page where the form was submitted."
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"
