from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from apps.core.validators import validate_image_file
from apps.ministries.models import Leader


def news_upload_path(instance, filename):
    return f"news/{filename}"


class NewsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "News Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ArticleQuerySet(models.QuerySet):
    def public(self):
        """
        Articles visible to the public: status is 'published' AND their
        scheduled publish time (if any) has already passed. This single
        method is what makes 'scheduled publication' work — an article
        can be set to 'published' today for a publish_date next Tuesday,
        and it simply won't appear here until that moment, with zero
        extra machinery (no cron job, no Celery task) required.
        """
        return self.filter(
            status=Article.Status.PUBLISHED,
            publish_date__lte=timezone.now(),
        )


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    excerpt = models.CharField(
        max_length=300, blank=True,
        help_text="Short summary shown in listings and homepage preview. "
                   "If left blank, the body's opening words are used instead.",
    )
    body = models.TextField()
    featured_image = models.ImageField(
        upload_to=news_upload_path, blank=True, null=True,
        validators=[validate_image_file],
    )

    # Public-facing byline — same Leader-vs-User split established for
    # Sermon.speaker in Phase 7. Optional: not every article needs a
    # named author displayed.
    author = models.ForeignKey(
        Leader, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles",
    )
    category = models.ForeignKey(
        NewsCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles",
    )

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    publish_date = models.DateTimeField(
        default=timezone.now,
        help_text="When this article should go live. Set to a future date/time "
                   "with status 'Published' to schedule it.",
    )
    is_featured = models.BooleanField(default=False)

    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="articles_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="articles_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ArticleQuerySet.as_manager()

    class Meta:
        ordering = ["-publish_date"]

    def __str__(self):
        return self.title

    @property
    def display_excerpt(self):
        if self.excerpt:
            return self.excerpt
        from django.utils.text import Truncator
        return Truncator(self.body).words(30)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)