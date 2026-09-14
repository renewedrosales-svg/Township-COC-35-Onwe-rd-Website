from django.conf import settings
from django.db import models
from django.utils.text import slugify

from apps.core.validators import validate_image_file
from apps.events.models import Event


def gallery_upload_path(instance, filename):
    return f"gallery/{filename}"


class GalleryPhoto(models.Model):
    """
    A single photo on the public Gallery page. Replaces the earlier
    Album/Image structure (Phase 10) with a flat, individually
    categorized and publishable model per the Gallery redesign —
    each photo stands alone, no album grouping or click-through.
    """
    CATEGORY_CHOICES = [
        ("worship", "Worship"),
        ("community", "Community"),
        ("events", "Events"),
        ("ministries", "Ministries"),
        ("outreach", "Outreach"),
        ("special_moments", "Special Moments"),
        ("church_life", "Church Life"),
        ("bible_studies", "Bible Studies"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    image = models.ImageField(
        upload_to=gallery_upload_path,
        validators=[validate_image_file],
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    alt_text = models.CharField(
        max_length=255, blank=True,
        help_text="Describes the image for screen readers. If left blank, the title is used instead.",
    )
    event = models.ForeignKey(
        Event, on_delete=models.SET_NULL, null=True, blank=True, related_name="gallery_photos",
        help_text="Optional — link this photo to the event it was taken at.",
    )
    photo_date = models.DateField(help_text="Date shown on the photo card.")

    is_featured = models.BooleanField(
        default=False, help_text="Featured photos are prioritized in homepage previews.",
    )
    is_published = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="gallery_photos_created",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-photo_date"]

    def __str__(self):
        return self.title

    @property
    def display_alt(self):
        return self.alt_text or self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while GalleryPhoto.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)