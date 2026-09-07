from django.utils import timezone
from django.views.generic import DetailView, ListView

from .models import Event


class EventListView(ListView):
    model = Event
    template_name = "events/list.html"
    context_object_name = "upcoming_events"
    paginate_by = 9

    def get_queryset(self):
        today = timezone.localdate()
        return (
            Event.objects.filter(is_published=True, event_date__gte=today)
            .order_by("event_date", "start_time")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        context["past_events"] = (
            Event.objects.filter(is_published=True, event_date__lt=today)
            .order_by("-event_date")[:6]
        )
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "events/detail.html"
    context_object_name = "event"

    def get_queryset(self):
        return Event.objects.filter(is_published=True)