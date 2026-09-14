from django.utils import timezone
from django.views.generic import TemplateView

from apps.events.models import Event
from apps.gallery.models import GalleryPhoto
from apps.ministries.models import Ministry
from apps.news.models import Article
from apps.sermons.models import Sermon

from .models import CreedItem, HomepageContent

from apps.school.models import SchoolInfo

class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["homepage_content"] = HomepageContent.load()
        context["creed_items"] = CreedItem.objects.filter(is_active=True)

        content = context["homepage_content"]

        if content.show_events_section:
            context["upcoming_events"] = (
                Event.objects.filter(is_published=True, event_date__gte=timezone.localdate())
                .order_by("event_date", "start_time")[:3]
            )

        if content.show_sermons_section:
            context["latest_sermons"] = (
                Sermon.objects.filter(is_published=True)
                .select_related("speaker")
                .order_by("-date_delivered")[:3]
            )

        if content.show_ministries_section:
            featured = Ministry.objects.filter(is_active=True, is_featured=True)
            context["preview_ministries"] = featured if featured.exists() else Ministry.objects.filter(is_active=True)[:6]

        if content.show_news_section:
            context["latest_articles"] = (
                Article.objects.public()
                .select_related("category")
                .order_by("-publish_date")[:3]
            )

        if content.show_gallery_section:
            context["preview_photos"] = (
                GalleryPhoto.objects.filter(is_published=True)
                .order_by("-photo_date", "order")[:8]
            )

        if content.show_school_section:
            context["school_info"] = SchoolInfo.load()

        return context