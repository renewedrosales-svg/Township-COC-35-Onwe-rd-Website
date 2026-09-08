from django.urls import path

from .views import AboutView, ContactView, PageDetailView, SupportView

app_name = "pages"

urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("support/", SupportView.as_view(), name="support"),
    path("<slug:slug>/", PageDetailView.as_view(), name="detail"),
]