from django.views.generic import TemplateView

from apps.core.mixins import ChurchAdminRequiredMixin


class DashboardIndexView(ChurchAdminRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"