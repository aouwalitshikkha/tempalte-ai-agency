from django.db import models
from django.utils.text import slugify
from django.core.validators import MinLengthValidator


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
    is_active = models.BooleanField(
        default=False,
        help_text="Set to True to make this service Details visible on the site."
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


# Details are stored in a OneToOne model so the main Service table remains narrow.
class ServiceDetails(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, related_name='details')

    # HERO AREA
    hero_h1 = models.CharField(max_length=200, blank=True, help_text="Main H1 for hero area Separate with / for highlighting")
    hero_tagline = models.TextField( blank=True, help_text="Short tagline under the H1")

    # SHORT-DETAILS AREA (single title + image, bullet points in a separate model)
    short_section_title = models.CharField(max_length=200, blank=True, help_text="Main H2 for hero area Separate with / for highlighting")
    short_section_details = models.TextField(blank=True, help_text="Detailed description shown beside the bullet points.")
    short_section_image = models.ImageField(
        upload_to='service_short_images/',
        null=True,
        blank=True,
        help_text="Image shown beside the short details (like illustration/card)"
    )

    # metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service Details"
        verbose_name_plural = "Service Details"

    @property
    def split_short_title(self):
        """
        Split the short_section_title at the last '/' to allow multi-line display.
        Example: 'Complete SEO Automation / For Your Business'
                -> ('Complete SEO Automation', 'For Your Business')
        """
        if self.short_section_title and "/" in self.short_section_title:
            parts = self.short_section_title.rsplit("/", 1)
            return parts[0].strip(), parts[1].strip()
        return self.short_section_title, ""
    
    @property
    def split_hero_h1(self):

        if "/" in self.hero_h1:
            parts = self.hero_h1.rsplit("/", 1)
            return parts[0].strip(), parts[1].strip()
        return self.hero_h1, ""  # if no slash found

    def __str__(self):
        return f"Details for {self.service.service_name}"


# Bullet points for the short-details area: name + description
class BulletPointServices(models.Model):
    details = models.ForeignKey(ServiceDetails, on_delete=models.CASCADE, related_name='bullet_points')
    order = models.PositiveSmallIntegerField(default=0, help_text="Order for display (lower first)")
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, validators=[MinLengthValidator(0)])

    class Meta:
        ordering = ['order']
        verbose_name = "Bullet Point"
        verbose_name_plural = "Bullet Points"

    def __str__(self):
        return f"{self.title} ({self.details.service.service_name})"


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



class SubService(models.Model):
    """
    Represents individual sub-services under a main Service.
    Example: Under 'SEO Automation' → 'Technical SEO Audit', 'Content Optimization', etc.
    """
    parent_service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='sub_services',
        help_text="Main service this sub-service belongs to."
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)

    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-cog",
        help_text="FontAwesome icon class (e.g., 'fa-solid fa-chart-line')."
    )

    # Optional accent color theme
    color_theme = models.CharField(
        max_length=50,
        choices=[
            ('accent', 'Accent / Blue'),
            ('green', 'Green'),
            ('purple', 'Purple'),
            ('yellow', 'Yellow'),
            ('red', 'Red'),
        ],
        default='accent',
        help_text="Controls the color background of the sub-service section."
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0, help_text="Order of appearance in the section")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sub Service"
        verbose_name_plural = "Sub Services"
        ordering = ["parent_service", "order"]

    def __str__(self):
        return f"{self.title} ({self.parent_service.service_name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while SubService.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class SubServiceFeature(models.Model):
    sub_service = models.ForeignKey(
        SubService,
        on_delete=models.CASCADE,
        related_name="features"
    )
    text = models.CharField(max_length=255)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Sub Service Feature"
        verbose_name_plural = "Sub Service Features"

    def __str__(self):
        return f"{self.text} ({self.sub_service.title})"


from django.core.exceptions import ValidationError

class FAQ(models.Model):
    """
    Frequently Asked Questions — linked to either a main Service or a SubService.
    """
    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='faqs',
        null=True,
        blank=True,
        help_text="Attach this FAQ to a main service."
    )
    sub_service = models.ForeignKey(
        'SubService',
        on_delete=models.CASCADE,
        related_name='faqs',
        null=True,
        blank=True,
        help_text="Attach this FAQ to a sub-service."
    )

    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['order', 'created_at']

    def __str__(self):
        if self.sub_service:
            return f"FAQ ({self.sub_service.title}): {self.question[:40]}"
        elif self.service:
            return f"FAQ ({self.service.service_name}): {self.question[:40]}"
        return self.question

    def clean(self):
        # Ensure it's attached to *either* a Service or a SubService, not both
        if not self.service and not self.sub_service:
            raise ValidationError("You must link this FAQ to either a Service or a SubService.")
        if self.service and self.sub_service:
            raise ValidationError("An FAQ cannot be linked to both a Service and a SubService.")
