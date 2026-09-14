from django.contrib.sitemaps import Sitemap
from django.utils import timezone

from apps.events.models import Event

from apps.ministries.models import Ministry
from apps.news.models import Article
from apps.pages.models import Page
from apps.sermons.models import Sermon


class StaticViewSitemap(Sitemap):
    """
    The site's fixed, always-present pages that don't come from a
    model — home, about, ministries list, teachings list, events list,
    news list, gallery list, contact, support, school. Each entry is a
    URL name, not a path, so this stays correct even if a route's
    actual path segment ever changes.
    """
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home", "pages:about", "ministries:list", "sermons:list",
            "events:list", "news:list", "gallery:list", "pages:contact",
            "pages:support", "school:index",
        ]

    def location(self, item):
        from django.urls import reverse
        return reverse(item)


class MinistrySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Ministry.objects.filter(is_active=True)

    def location(self, obj):
        from django.urls import reverse
        return reverse("ministries:detail", args=[obj.slug])


class SermonSitemap(Sitemap):
    changefreq = "never"  # a published teaching's content doesn't change after the fact
    priority = 0.6

    def items(self):
        return Sermon.objects.filter(is_published=True)

    def location(self, obj):
        from django.urls import reverse
        return reverse("sermons:detail", args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at


class EventSitemap(Sitemap):
    changefreq = "daily"  # upcoming events can get registration/detail edits close to the date
    priority = 0.7

    def items(self):
        return Event.objects.filter(is_published=True)

    def location(self, obj):
        from django.urls import reverse
        return reverse("events:detail", args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at


class ArticleSitemap(Sitemap):
    changefreq = "never"
    priority = 0.6

    def items(self):
        return Article.objects.public()

    def location(self, obj):
        from django.urls import reverse
        return reverse("news:detail", args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at


class GalleryPhotoSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.3

    def items(self):
        return []  # individual photos have no standalone URL to list; the gallery list page itself is covered by StaticViewSitemap
    

class FlatPageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Page.objects.filter(is_published=True)

    def location(self, obj):
        from django.urls import reverse
        return reverse("pages:detail", args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at