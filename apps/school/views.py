from django.views.generic import TemplateView

from .models import SchoolInfo


class SchoolView(TemplateView):
    template_name = "school/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["school_info"] = SchoolInfo.load()
        return context