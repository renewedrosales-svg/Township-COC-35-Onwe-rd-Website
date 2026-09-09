from django.views.generic import TemplateView

from apps.core.media_library import get_media_items
from apps.core.mixins import ChurchAdminRequiredMixin


class DashboardMediaLibraryView(ChurchAdminRequiredMixin, TemplateView):
    template_name = "dashboard/media/library.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_items"] = get_media_items()
        return context