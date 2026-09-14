from django.urls import path

from .views import EventDetailView, EventListView, event_ics_download

app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="list"),
    path("<slug:slug>/calendar.ics", event_ics_download, name="ics_download"),
    path("<slug:slug>/", EventDetailView.as_view(), name="detail"),
]