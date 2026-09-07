from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from .views import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health_check"),
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
]