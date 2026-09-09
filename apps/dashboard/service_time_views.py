from django.urls import reverse_lazy

from apps.church_settings.forms import ServiceTimeForm
from apps.church_settings.models import ServiceTime
from apps.core.dashboard_views import (
    DashboardCreateView,
    DashboardDeleteView,
    DashboardListView,
    DashboardUpdateView,
)


class DashboardServiceTimeListView(DashboardListView):
    model = ServiceTime
    template_name = "dashboard/church_settings/service_time_list.html"
    context_object_name = "service_times"

    def get_queryset(self):
        return ServiceTime.objects.order_by("order", "day", "start_time")


class DashboardServiceTimeCreateView(DashboardCreateView):
    model = ServiceTime
    form_class = ServiceTimeForm
    success_url = reverse_lazy("dashboard:service_time_list")


class DashboardServiceTimeUpdateView(DashboardUpdateView):
    model = ServiceTime
    form_class = ServiceTimeForm
    success_url = reverse_lazy("dashboard:service_time_list")


class DashboardServiceTimeDeleteView(DashboardDeleteView):
    model = ServiceTime
    success_url = reverse_lazy("dashboard:service_time_list")