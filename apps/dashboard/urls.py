from django.urls import path

from .sermon_views import (
    DashboardSermonCreateView,
    DashboardSermonDeleteView,
    DashboardSermonListView,
    DashboardSermonUpdateView,
)
from .views import DashboardIndexView

from .event_views import DashboardEventCreateView, DashboardEventDeleteView, DashboardEventListView, DashboardEventUpdateView
from .gallery_views import DashboardAlbumCreateView, DashboardAlbumDeleteView, DashboardAlbumListView, DashboardAlbumUpdateView
from .ministry_views import (
    DashboardLeaderCreateView, DashboardLeaderDeleteView, DashboardLeaderListView, DashboardLeaderUpdateView,
    DashboardMinistryCreateView, DashboardMinistryDeleteView, DashboardMinistryListView, DashboardMinistryUpdateView,
)
from .news_views import DashboardArticleCreateView, DashboardArticleDeleteView, DashboardArticleListView, DashboardArticleUpdateView
from .page_views import DashboardPageCreateView, DashboardPageDeleteView, DashboardPageListView, DashboardPageUpdateView

from .church_settings_views import DashboardChurchSettingsView, DashboardSEODefaultsView
from .media_views import DashboardMediaLibraryView
from .service_time_views import (
    DashboardServiceTimeCreateView,
    DashboardServiceTimeDeleteView,
    DashboardServiceTimeListView,
    DashboardServiceTimeUpdateView,
)
from .school_views import DashboardSchoolInfoView


app_name = "dashboard"

urlpatterns = [
    path("", DashboardIndexView.as_view(), name="index"),
    path("teachings/", DashboardSermonListView.as_view(), name="sermon_list"),
    path("teachings/new/", DashboardSermonCreateView.as_view(), name="sermon_create"),
    path("teachings/<slug:slug>/edit/", DashboardSermonUpdateView.as_view(), name="sermon_update"),
    path("teachings/<slug:slug>/delete/", DashboardSermonDeleteView.as_view(), name="sermon_delete"),
]


urlpatterns += [
    path("ministries/", DashboardMinistryListView.as_view(), name="ministry_list"),
    path("ministries/new/", DashboardMinistryCreateView.as_view(), name="ministry_create"),
    path("ministries/<slug:slug>/edit/", DashboardMinistryUpdateView.as_view(), name="ministry_update"),
    path("ministries/<slug:slug>/delete/", DashboardMinistryDeleteView.as_view(), name="ministry_delete"),

    path("leaders/", DashboardLeaderListView.as_view(), name="leader_list"),
    path("leaders/new/", DashboardLeaderCreateView.as_view(), name="leader_create"),
    path("leaders/<int:pk>/edit/", DashboardLeaderUpdateView.as_view(), name="leader_update"),
    path("leaders/<int:pk>/delete/", DashboardLeaderDeleteView.as_view(), name="leader_delete"),

    path("pages/", DashboardPageListView.as_view(), name="page_list"),
    path("pages/new/", DashboardPageCreateView.as_view(), name="page_create"),
    path("pages/<slug:slug>/edit/", DashboardPageUpdateView.as_view(), name="page_update"),
    path("pages/<slug:slug>/delete/", DashboardPageDeleteView.as_view(), name="page_delete"),

    path("events/", DashboardEventListView.as_view(), name="event_list"),
    path("events/new/", DashboardEventCreateView.as_view(), name="event_create"),
    path("events/<slug:slug>/edit/", DashboardEventUpdateView.as_view(), name="event_update"),
    path("events/<slug:slug>/delete/", DashboardEventDeleteView.as_view(), name="event_delete"),

    path("news/", DashboardArticleListView.as_view(), name="article_list"),
    path("news/new/", DashboardArticleCreateView.as_view(), name="article_create"),
    path("news/<slug:slug>/edit/", DashboardArticleUpdateView.as_view(), name="article_update"),
    path("news/<slug:slug>/delete/", DashboardArticleDeleteView.as_view(), name="article_delete"),

    path("gallery/", DashboardAlbumListView.as_view(), name="album_list"),
    path("gallery/new/", DashboardAlbumCreateView.as_view(), name="album_create"),
    path("gallery/<slug:slug>/edit/", DashboardAlbumUpdateView.as_view(), name="album_update"),
    path("gallery/<slug:slug>/delete/", DashboardAlbumDeleteView.as_view(), name="album_delete"),

        path("settings/", DashboardChurchSettingsView.as_view(), name="church_settings"),
    path("settings/seo/", DashboardSEODefaultsView.as_view(), name="seo_defaults"),

    path("service-times/", DashboardServiceTimeListView.as_view(), name="service_time_list"),
    path("service-times/new/", DashboardServiceTimeCreateView.as_view(), name="service_time_create"),
    path("service-times/<int:pk>/edit/", DashboardServiceTimeUpdateView.as_view(), name="service_time_update"),
    path("service-times/<int:pk>/delete/", DashboardServiceTimeDeleteView.as_view(), name="service_time_delete"),

    path("media/", DashboardMediaLibraryView.as_view(), name="media_library"),
    path("school/", DashboardSchoolInfoView.as_view(), name="school_info"),

]