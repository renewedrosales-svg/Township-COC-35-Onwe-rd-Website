from django.urls import path

from .views import TeachingDetailView, TeachingListView

app_name = "sermons"

urlpatterns = [
    path("", TeachingListView.as_view(), name="list"),
    path("<slug:slug>/", TeachingDetailView.as_view(), name="detail"),
]