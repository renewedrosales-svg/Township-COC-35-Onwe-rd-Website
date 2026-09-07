from django.conf import settings
from django.db import models
from django.utils.text import slugify

from apps.core.validators import validate_image_file


def ministries_upload_path(instance, filename):
    return f"ministries/{filename}"


class Leader(models.Model):
    """
    Public leadership/minister profile per §14. Optionally linked to a
    User account (for Ministers who log into the CMS) — but stands
    alone for leaders who don't (elders, deacons). Only intentionally
    published fields are ever public; there is no private-info field
    on this model at all, by design, so there's nothing to accidentally
    leak.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="leader_profile",
        help_text="Link to a CMS login only if this leader is also a Minister who signs in.",
    )
    full_name = models.CharField(max_length=200)
    position_title = models.CharField(max_length=150, help_text="e.g. 'Senior Minister', 'Elder'")
    photo = models.ImageField(
        upload_to=ministries_upload_path, blank=True, null=True,
        validators=[validate_image_file],
    )
    bio = models.TextField(blank=True)
    public_email = models.EmailField(blank=True, help_text="Only shown publicly if filled in.")
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Inactive leaders are hidden from the public site.")

    class Meta:
        ordering = ["display_order", "full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.position_title})"


class Ministry(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=ministries_upload_path, blank=True, null=True,
        validators=[validate_image_file],
    )
    leader = models.ForeignKey(
        Leader, on_delete=models.SET_NULL, null=True, blank=True, related_name="ministries_led",
    )
    meeting_info = models.CharField(
        max_length=255, blank=True, help_text="e.g. 'Saturdays, 4:00 PM, Fellowship Hall'",
    )
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="ministries_created",
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Ministries"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)