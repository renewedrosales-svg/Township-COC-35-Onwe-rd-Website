from django.urls import reverse_lazy

from apps.core.dashboard_views import (
    DashboardCreateView,
    DashboardDeleteView,
    DashboardListView,
    DashboardUpdateView,
)
from apps.events.forms import EventForm
from apps.events.models import Event


class DashboardEventListView(DashboardListView):
    model = Event
    template_name = "dashboard/events/list.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.order_by("-event_date")


class DashboardEventCreateView(DashboardCreateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy("dashboard:event_list")


class DashboardEventUpdateView(DashboardUpdateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy("dashboard:event_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"


class DashboardEventDeleteView(DashboardDeleteView):
    model = Event
    success_url = reverse_lazy("dashboard:event_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"