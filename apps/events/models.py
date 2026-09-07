from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


def events_upload_path(instance, filename):
    return f"events/{filename}"


class Event(models.Model):
    from apps.core.validators import validate_image_file

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    description = models.TextField(blank=True)

    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)

    image = models.ImageField(
        upload_to=events_upload_path, blank=True, null=True,
        validators=[validate_image_file],
    )
    organizer = models.CharField(
        max_length=150, blank=True, help_text="e.g. 'Youth Ministry', 'Church Office'",
    )
    registration_info = models.TextField(
        blank=True, help_text="Instructions if registration is required, e.g. 'RSVP at the church office by Friday.'",
    )
    external_link = models.URLField(
        blank=True, help_text="Optional link — registration form, more info, livestream, etc.",
    )

    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="events_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["event_date", "start_time"]

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        return self.event_date < timezone.localdate()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)