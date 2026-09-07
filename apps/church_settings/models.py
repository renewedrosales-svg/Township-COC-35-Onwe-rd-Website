from django.db import models

from apps.core.models import SingletonModel
from apps.core.validators import validate_image_file


def church_upload_path(instance, filename):
    return f"church_settings/{filename}"


class ChurchSettings(SingletonModel):
    # Identity
    church_name = models.CharField(
        max_length=255, default="35 Onwe Road Church of Christ"
    )
    tagline = models.CharField(
        max_length=255, blank=True,
        help_text="Short phrase shown near the church name, e.g. in the footer.",
    )
    logo = models.ImageField(
        upload_to=church_upload_path, blank=True, null=True,
        validators=[validate_image_file],
    )
    favicon = models.ImageField(
        upload_to=church_upload_path, blank=True, null=True,
        validators=[validate_image_file],
    )

    # Contact
    address = models.CharField(max_length=500, blank=True)
    phone_primary = models.CharField(max_length=50, blank=True)
    phone_secondary = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    # Social links — only the platforms named in §52; left blank = not shown
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    whatsapp_url = models.URLField(blank=True)
    x_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)

    # Map — deliberately a restricted, validated embed URL, not raw HTML
    # (per §53 — never allow arbitrary unsafe embeds)
    map_embed_url = models.URLField(
        blank=True,
        help_text="Paste a Google Maps 'Embed a map' src URL only.",
    )

    # Footer
    footer_short_description = models.TextField(blank=True)

    # Default SEO (per-page SEO fields come later, in each content app;
    # these are the sitewide fallback per §35/§49)
    default_seo_title = models.CharField(max_length=255, blank=True)
    default_seo_description = models.CharField(max_length=300, blank=True)
    default_og_image = models.ImageField(
        upload_to=church_upload_path, blank=True, null=True,
        validators=[validate_image_file],
    )

    class Meta:
        verbose_name = "Church Settings"
        verbose_name_plural = "Church Settings"

    def __str__(self):
        return self.church_name

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.map_embed_url and "google.com/maps/embed" not in self.map_embed_url:
            raise ValidationError(
                {"map_embed_url": "Only Google Maps embed URLs are accepted "
                                   "(must contain 'google.com/maps/embed')."}
            )


class ServiceTime(models.Model):
    DAY_CHOICES = [
        ("monday", "Monday"), ("tuesday", "Tuesday"), ("wednesday", "Wednesday"),
        ("thursday", "Thursday"), ("friday", "Friday"), ("saturday", "Saturday"),
        ("sunday", "Sunday"),
    ]

    name = models.CharField(max_length=100, help_text="e.g. 'Sunday Worship Service'")
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers display first.")

    class Meta:
        ordering = ["order", "day", "start_time"]
        verbose_name = "Service Time"
        verbose_name_plural = "Service Times"

    def __str__(self):
        return f"{self.name} — {self.get_day_display()}"