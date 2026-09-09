from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from .views import health_check
from apps.accounts.forms import StyledLoginForm

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health_check"),

    path("login/", auth_views.LoginView.as_view(template_name="pages/login.html", authentication_form=StyledLoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("dashboard/", include("apps.dashboard.urls")),

    path("", include("apps.homepage.urls")),
    path("ministries/", include("apps.ministries.urls")),
    path("teachings/", include("apps.sermons.urls")),
    path("events/", include("apps.events.urls")),
    path("news/", include("apps.news.urls")),
    path("gallery/", include("apps.gallery.urls")),
    path("school/", include("apps.school.urls")),

    # pages.urls MUST stay LAST — catch-all "<slug:slug>/" pattern.
    # contact/ and school/ get added ABOVE this line in their own phases.
    path("", include("apps.pages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)