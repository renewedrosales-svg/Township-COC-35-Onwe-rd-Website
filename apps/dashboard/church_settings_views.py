from django.urls import reverse_lazy

from apps.church_settings.forms import ChurchSettingsForm, SEODefaultsForm
from apps.church_settings.models import ChurchSettings
from apps.core.dashboard_views import (
    DashboardCreateView,
    DashboardDeleteView,
    DashboardListView,
    DashboardSingletonUpdateView,
    DashboardUpdateView,
)


class DashboardChurchSettingsView(DashboardSingletonUpdateView):
    singleton_model = ChurchSettings
    form_class = ChurchSettingsForm
    success_url = reverse_lazy("dashboard:church_settings")
    page_title = "Church Settings"


class DashboardSEODefaultsView(DashboardSingletonUpdateView):
    singleton_model = ChurchSettings
    form_class = SEODefaultsForm
    success_url = reverse_lazy("dashboard:seo_defaults")
    page_title = "SEO Defaults"