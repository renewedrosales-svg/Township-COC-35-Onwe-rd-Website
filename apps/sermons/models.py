from django.conf import settings
from django.db import models
from django.utils.text import slugify

from apps.core.validators import (
    validate_audio_file,
    validate_image_file,
    validate_pdf_file,
)
from apps.ministries.models import Leader


def sermons_upload_path(instance, filename):
    return f"sermons/{filename}"


class SermonCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Sermon Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Sermon(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)

    # Public-facing speaker identity (photo/bio) — distinct from
    # `created_by` below, same pattern established in Phase 6 for
    # Leader vs. User. A guest speaker with no CMS login can still be
    # credited here.
    speaker = models.ForeignKey(
        Leader, on_delete=models.SET_NULL, null=True, blank=True, related_name="sermons",
    )
    date_delivered = models.DateField()
    scripture_reference = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        SermonCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="sermons",
    )

    thumbnail = models.ImageField(
        upload_to=sermons_upload_path, blank=True, null=True,
        validators=[validate_image_file],
    )
    audio_file = models.FileField(
        upload_to=sermons_upload_path, blank=True, null=True,
        validators=[validate_audio_file],
    )
    video_url = models.URLField(
        blank=True, help_text="YouTube/Vimeo link. We embed external video rather than hosting it ourselves.",
    )
    notes_pdf = models.FileField(
        upload_to=sermons_upload_path, blank=True, null=True,
        validators=[validate_pdf_file],
        help_text="Sermon notes as a downloadable PDF.",
    )

    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    # Ownership — this is what OwnerOrElevatedRequiredMixin (Phase 3)
    # checks against. A Minister may only edit/delete sermons where
    # created_by == themself; Church Admin/Super Admin bypass this.
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="sermons_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_delivered"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Sermon.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)