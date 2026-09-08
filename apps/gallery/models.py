from django.conf import settings
from django.db import models
from django.utils.text import slugify

from apps.core.validators import validate_image_file
from apps.events.models import Event


def gallery_upload_path(instance, filename):
    # instance here is a GalleryImage; group files by album for tidier
    # storage browsing, matching the date-bucketing spirit of §11
    # without needing actual date logic for what's typically a
    # bounded, event-driven set of uploads.
    album_slug = instance.album.slug if instance.album_id else "unsorted"
    return f"gallery/{album_slug}/{filename}"


class GalleryAlbum(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)

    event = models.ForeignKey(
        Event, on_delete=models.SET_NULL, null=True, blank=True, related_name="gallery_albums",
        help_text="Optional — link this album to the event it was taken at.",
    )

    is_published = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="albums_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def cover_image(self):
        """
        The album's representative thumbnail: the image explicitly
        marked featured, or failing that, the first image in the
        album. Avoids needing a separate 'cover_image' upload field
        that editors would have to remember to set independently of
        the images they've actually uploaded.
        """
        featured = self.images.filter(is_featured=True).first()
        return featured or self.images.first()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while GalleryAlbum.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)


class GalleryImage(models.Model):
    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        upload_to=gallery_upload_path,
        validators=[validate_image_file],
    )
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(
        max_length=255, blank=True,
        help_text="Describes the image for screen readers. If left blank, the caption is used instead.",
    )
    is_featured = models.BooleanField(
        default=False, help_text="Featured images are used as the album cover and in homepage previews.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Image #{self.pk} in {self.album.title}"

    @property
    def display_alt(self):
        return self.alt_text or self.caption or self.album.title