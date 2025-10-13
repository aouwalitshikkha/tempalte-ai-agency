from django.db import models
from django.utils.text import slugify


# -------------------------------
# 1️⃣ MAIN SERVICE (PARENT)
# -------------------------------
class MainService(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(upload_to="services/main/", blank=True, null=True)
    ranking = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['ranking']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.ranking:
            self.ranking = MainService.objects.count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# -------------------------------
# 2️⃣ SUB SERVICE (UNDER MAIN SERVICE)
# -------------------------------
class SubService(models.Model):
    main_service = models.ForeignKey(MainService, related_name="subservices", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    conclusion = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(upload_to="services/sub/", blank=True, null=True)
    ranking = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ranking']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.ranking:
            self.ranking = SubService.objects.filter(main_service=self.main_service).count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.main_service.title})"


# -------------------------------
# 3️⃣ FEATURES UNDER EACH SUB SERVICE
# -------------------------------
class SubServiceFeature(models.Model):
    sub_service = models.ForeignKey(SubService, related_name="features", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True, help_text="SVG or icon class name")
    ranking = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ranking']

    def __str__(self):
        return f"{self.title} - {self.sub_service.title}"


# -------------------------------
# 4️⃣ PRICING PLANS FOR EACH SUB SERVICE
# -------------------------------
class Pricing(models.Model):
    sub_service = models.ForeignKey(SubService, related_name="pricing_plans", on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. per month, one-time")
    description = models.TextField(blank=True, null=True)
    features = models.TextField(blank=True, help_text="Use bullet points or HTML list")
    is_popular = models.BooleanField(default=False)
    ranking = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ranking']

    def __str__(self):
        return f"{self.plan_name} - {self.sub_service.title}"


# -------------------------------
# 5️⃣ FAQ SECTION
# -------------------------------
class FAQ(models.Model):
    sub_service = models.ForeignKey(SubService, related_name="faqs", on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question


# -------------------------------
# 6️⃣ TRUSTED COMPANIES (LOGOS)
# -------------------------------
class CompanyLogo(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="companies/logos/")
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name



# -------------------------------
# 7️⃣ TESTIMONIALS (GLOBAL / MAIN / SUB LEVEL)
# -------------------------------
class Testimonial(models.Model):
    # Level relationships
    main_service = models.ForeignKey(
        MainService,
        related_name="testimonials",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Attach to a specific Main Service (optional)"
    )
    sub_service = models.ForeignKey(
        SubService,
        related_name="testimonials",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Attach to a specific Sub Service (optional)"
    )

    # Content fields
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField()
    photo = models.ImageField(upload_to="testimonials/photos/", blank=True, null=True)

    # Display logic
    show_on_home = models.BooleanField(default=False, help_text="Show this testimonial on the Home Page")
    is_active = models.BooleanField(default=True)
    ranking = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ranking']

    def __str__(self):
        location = (
            self.sub_service.title if self.sub_service else
            self.main_service.title if self.main_service else
            "Global"
        )
        return f"{self.name} ({location})"
