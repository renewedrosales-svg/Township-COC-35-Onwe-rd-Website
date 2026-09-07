from django.views.generic import TemplateView

from apps.ministries.models import Ministry
from apps.sermons.models import Sermon

from .models import CreedItem, HomepageContent


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["homepage_content"] = HomepageContent.load()
        context["creed_items"] = CreedItem.objects.filter(is_active=True)

        content = context["homepage_content"]

        if content.show_ministries_section:
            featured = Ministry.objects.filter(is_active=True, is_featured=True)
            context["preview_ministries"] = featured if featured.exists() else Ministry.objects.filter(is_active=True)[:6]

        if content.show_sermons_section:
            context["latest_sermons"] = (
                Sermon.objects.filter(is_published=True)
                .select_related("speaker")
                .order_by("-date_delivered")[:3]
            )

        return context