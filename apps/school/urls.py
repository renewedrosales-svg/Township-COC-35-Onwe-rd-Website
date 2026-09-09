from django.urls import path

from .views import SchoolView

app_name = "school"

urlpatterns = [
    path("", SchoolView.as_view(), name="index"),
]