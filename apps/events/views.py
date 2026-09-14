import calendar as cal_module

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, ListView

from apps.core.ics import build_event_ics

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

        # Static current-month calendar grid for the sidebar (no
        # navigation, per project decision — just a visual reference
        # highlighting today and any day with a published event).
        calendar_obj = cal_module.Calendar(firstweekday=6)  # weeks start Sunday
        context["calendar_weeks"] = calendar_obj.monthdayscalendar(today.year, today.month)
        context["calendar_month_label"] = today.strftime("%B %Y")
        context["calendar_today_day"] = today.day
        context["calendar_event_days"] = set(
            Event.objects.filter(
                is_published=True, event_date__year=today.year, event_date__month=today.month,
            ).values_list("event_date__day", flat=True)
        )
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "events/detail.html"
    context_object_name = "event"

    def get_queryset(self):
        return Event.objects.filter(is_published=True)


def event_ics_download(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    ics_content = build_event_ics(event)
    response = HttpResponse(ics_content, content_type="text/calendar")
    response["Content-Disposition"] = f'attachment; filename="{event.slug}.ics"'
    return response