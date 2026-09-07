from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from apps.core.models import SingletonModel
from apps.core.validators import validate_image_file

RESERVED_SLUGS = {
    "admin", "dashboard", "login", "logout", "health", "static", "media",
    "about", "ministries", "sermons", "events", "news", "gallery",
    "contact", "school",
}


def pages_upload_path(instance, filename):
    return f"pages/{filename}"


class Page(models.Model):
    """
    Flat CMS-managed pages per §20 — Faith, Privacy, Terms, and any
    additional page an administrator creates. NOT used for About (which
    has its own structured model below, since it needs many distinct
    fields, not one body blob) or the homepage.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    body = models.TextField(
        help_text="Plain text/paragraphs. Rendered with line breaks preserved.",
    )
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)
    is_published = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="pages_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="pages_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def clean(self):
        if self.slug and self.slug in RESERVED_SLUGS:
            raise ValidationError({"slug": f"'{self.slug}' is a reserved URL and can't be used as a page slug."})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.full_clean()
        super().save(*args, **kwargs)


class AboutPageContent(SingletonModel):
    """
    Structured content for the About page (§13). A singleton because
    there is exactly one About page, but it needs distinct editable
    sections rather than a single free-text body.
    """
    hero_image = models.ImageField(
        upload_to=pages_upload_path, blank=True, null=True,
        validators=[validate_image_file],
    )
    who_we_are = models.TextField(blank=True)
    our_history = models.TextField(blank=True)
    our_mission = models.TextField(blank=True)
    our_vision = models.TextField(blank=True)
    our_values = models.TextField(blank=True)
    statement_of_faith = models.TextField(blank=True)

    show_leadership_section = models.BooleanField(
        default=True,
        help_text="Show the leadership/ministers listing on the About page.",
    )

    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"

    def __str__(self):
        return "About Page Content"