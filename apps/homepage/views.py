from django.views.generic import TemplateView

from .models import CreedItem, HomepageContent


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["homepage_content"] = HomepageContent.load()
        context["creed_items"] = CreedItem.objects.filter(is_active=True)
        return context