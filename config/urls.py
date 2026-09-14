from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.accounts.forms import StyledLoginForm
from apps.accounts.views import RateLimitAwareLoginView

from apps.core.sitemaps import (
    ArticleSitemap,
    EventSitemap,
    FlatPageSitemap,
    GalleryPhotoSitemap,
    MinistrySitemap,
    SermonSitemap,
    StaticViewSitemap,
)
from apps.core.views import custom_400, custom_403, custom_404, custom_500, robots_txt

from .views import health_check

sitemaps = {
    "static": StaticViewSitemap,
    "ministries": MinistrySitemap,
    "teachings": SermonSitemap,
    "events": EventSitemap,
    "news": ArticleSitemap,
    "gallery": GalleryPhotoSitemap,
    "pages": FlatPageSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health_check"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),

    path("login/", RateLimitAwareLoginView.as_view(template_name="pages/login.html", authentication_form=StyledLoginForm), name="login"),
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
    path("", include("apps.pages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = custom_400
handler403 = custom_403
handler404 = custom_404
handler500 = custom_500