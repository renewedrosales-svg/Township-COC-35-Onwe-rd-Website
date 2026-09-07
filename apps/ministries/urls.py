from django.urls import path

from .views import MinistryDetailView, MinistryListView

app_name = "ministries"

urlpatterns = [
    path("", MinistryListView.as_view(), name="list"),
    path("<slug:slug>/", MinistryDetailView.as_view(), name="detail"),
]