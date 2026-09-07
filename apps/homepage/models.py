from django.db import models

from apps.core.models import SingletonModel
from apps.core.validators import validate_image_file


def homepage_upload_path(instance, filename):
    return f"homepage/{filename}"


class HomepageContent(SingletonModel):
    # --- Hero section ---
    hero_eyebrow = models.CharField(
        max_length=100, blank=True,
        default="Welcome to 35 Onwe Road Church of Christ",
    )
    hero_headline = models.CharField(
        max_length=200, default="A Place to Worship, Grow and Serve",
        help_text="Main headline. Use the 'accent' field below for the "
                   "single word/phrase you want highlighted in gold.",
    )
    hero_headline_accent = models.CharField(
        max_length=50, blank=True,
        help_text="A word/phrase from the headline above to render in gold, e.g. 'Grow'.",
    )
    hero_description = models.TextField(
        blank=True,
        default="We are a community of believers passionate about worship, "
                "growing in God's Word, and reaching out with His love.",
    )
    hero_image = models.ImageField(
        upload_to=homepage_upload_path, blank=True, null=True,
        validators=[validate_image_file],
    )
    hero_cta_primary_text = models.CharField(max_length=50, default="Plan Your Visit")
    hero_cta_primary_url = models.CharField(max_length=255, blank=True, default="#visit")
    hero_cta_secondary_text = models.CharField(max_length=50, blank=True, default="Watch Sermons")
    hero_cta_secondary_url = models.CharField(max_length=255, blank=True, default="#")

    # --- About preview section ---
    about_eyebrow = models.CharField(max_length=100, blank=True, default="About Us")
    about_heading = models.CharField(max_length=200, blank=True, default="Faith. Family. Impact.")
    about_description = models.TextField(blank=True)
    about_image = models.ImageField(
        upload_to=homepage_upload_path, blank=True, null=True,
        validators=[validate_image_file],
    )
    about_cta_text = models.CharField(max_length=50, blank=True, default="Our Beliefs")
    about_cta_url = models.CharField(max_length=255, blank=True, default="#")

    # --- Visit Us CTA banner (closing section) ---
    visit_cta_heading = models.CharField(max_length=200, blank=True, default="Join Us This Sunday")
    visit_cta_description = models.TextField(blank=True)
    visit_cta_image = models.ImageField(
        upload_to=homepage_upload_path, blank=True, null=True,
        validators=[validate_image_file],
    )
    visit_cta_button_text = models.CharField(max_length=50, blank=True, default="Find Us")
    visit_cta_button_url = models.CharField(max_length=255, blank=True, default="#")

    # --- Section visibility toggles ---
    # Default False for sections whose backing app doesn't exist yet.
    # Flip to True (and wire the real queryset in the template) once that
    # app's phase is complete. See homepage/views.py for where each one
    # is consumed.
    show_creed_section = models.BooleanField(default=True)
    show_about_section = models.BooleanField(default=True)
    show_service_times_section = models.BooleanField(default=True)
    show_events_section = models.BooleanField(default=False)      # Phase 8
    show_sermons_section = models.BooleanField(default=False)     # Phase 7
    show_ministries_section = models.BooleanField(default=False)  # Phase 6
    show_news_section = models.BooleanField(default=False)        # Phase 9
    show_gallery_section = models.BooleanField(default=False)     # Phase 10
    show_school_section = models.BooleanField(default=False)      # Phase 13
    show_visit_cta_section = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Homepage Content"
        verbose_name_plural = "Homepage Content"

    def __str__(self):
        return "Homepage Content"


class CreedItem(models.Model):
    """
    A single value in the 'Our Creed' strip (e.g. True Worship, The Bible,
    Fellowship, Service — §12). Icon is chosen from a small fixed set
    rendered as inline SVG in the template, not an uploaded image — keeps
    this section fast-loading and visually consistent (§67: don't
    over-engineer a 4-item list with a full image upload pipeline).
    """
    ICON_CHOICES = [
        ("cross", "Cross"),
        ("book", "Book"),
        ("users", "People / Fellowship"),
        ("heart", "Heart / Service"),
    ]

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default="cross")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Creed Item"
        verbose_name_plural = "Creed Items"

    def __str__(self):
        return self.title