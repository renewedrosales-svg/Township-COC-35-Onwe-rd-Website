from django.urls import reverse_lazy

from apps.core.dashboard_views import (
    DashboardCreateView,
    DashboardDeleteView,
    DashboardListView,
    DashboardUpdateView,
)
from apps.ministries.forms import LeaderForm, MinistryForm
from apps.ministries.models import Leader, Ministry


class DashboardMinistryListView(DashboardListView):
    model = Ministry
    template_name = "dashboard/ministries/list.html"
    context_object_name = "ministries"

    def get_queryset(self):
        return Ministry.objects.select_related("leader").order_by("order", "name")


class DashboardMinistryCreateView(DashboardCreateView):
    model = Ministry
    form_class = MinistryForm
    success_url = reverse_lazy("dashboard:ministry_list")


class DashboardMinistryUpdateView(DashboardUpdateView):
    model = Ministry
    form_class = MinistryForm
    success_url = reverse_lazy("dashboard:ministry_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"


class DashboardMinistryDeleteView(DashboardDeleteView):
    model = Ministry
    success_url = reverse_lazy("dashboard:ministry_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"


class DashboardLeaderListView(DashboardListView):
    model = Leader
    template_name = "dashboard/ministries/leader_list.html"
    context_object_name = "leaders"

    def get_queryset(self):
        return Leader.objects.order_by("display_order", "full_name")


class DashboardLeaderCreateView(DashboardCreateView):
    model = Leader
    form_class = LeaderForm
    success_url = reverse_lazy("dashboard:leader_list")


class DashboardLeaderUpdateView(DashboardUpdateView):
    model = Leader
    form_class = LeaderForm
    success_url = reverse_lazy("dashboard:leader_list")


class DashboardLeaderDeleteView(DashboardDeleteView):
    model = Leader
    success_url = reverse_lazy("dashboard:leader_list")