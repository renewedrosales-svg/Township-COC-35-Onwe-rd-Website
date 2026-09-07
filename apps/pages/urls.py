from django.urls import path

from .views import AboutView, PageDetailView

app_name = "pages"

urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
    path("<slug:slug>/", PageDetailView.as_view(), name="detail"),
]