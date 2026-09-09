from django.urls import reverse_lazy

from apps.core.dashboard_views import (
    DashboardCreateView,
    DashboardDeleteView,
    DashboardListView,
    DashboardUpdateView,
)
from apps.pages.forms import PageForm
from apps.pages.models import Page


class DashboardPageListView(DashboardListView):
    model = Page
    template_name = "dashboard/pages/list.html"
    context_object_name = "pages"

    def get_queryset(self):
        return Page.objects.order_by("title")


class DashboardPageCreateView(DashboardCreateView):
    model = Page
    form_class = PageForm
    success_url = reverse_lazy("dashboard:page_list")


class DashboardPageUpdateView(DashboardUpdateView):
    model = Page
    form_class = PageForm
    success_url = reverse_lazy("dashboard:page_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"


class DashboardPageDeleteView(DashboardDeleteView):
    model = Page
    success_url = reverse_lazy("dashboard:page_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"