from django.urls import path

from .church_settings_views import DashboardChurchSettingsView, DashboardNotificationSettingsView, DashboardSEODefaultsView
from .event_views import DashboardEventCreateView, DashboardEventDeleteView, DashboardEventListView, DashboardEventUpdateView
from .gallery_views import (
    DashboardGalleryPhotoCreateView,
    DashboardGalleryPhotoDeleteView,
    DashboardGalleryPhotoListView,
    DashboardGalleryPhotoUpdateView,
)
from .media_views import DashboardMediaLibraryView
from .ministry_views import (
    DashboardLeaderCreateView, DashboardLeaderDeleteView, DashboardLeaderListView, DashboardLeaderUpdateView,
    DashboardMinistryCreateView, DashboardMinistryDeleteView, DashboardMinistryListView, DashboardMinistryUpdateView,
)
from .news_views import DashboardArticleCreateView, DashboardArticleDeleteView, DashboardArticleListView, DashboardArticleUpdateView
from .page_views import DashboardPageCreateView, DashboardPageDeleteView, DashboardPageListView, DashboardPageUpdateView
from .school_views import DashboardSchoolInfoView
from .sermon_views import (
    DashboardSermonCreateView,
    DashboardSermonDeleteView,
    DashboardSermonListView,
    DashboardSermonUpdateView,
)
from .service_time_views import (
    DashboardServiceTimeCreateView,
    DashboardServiceTimeDeleteView,
    DashboardServiceTimeListView,
    DashboardServiceTimeUpdateView,
)
from .support_views import (
    DashboardBankAccountCreateView,
    DashboardBankAccountDeleteView,
    DashboardBankAccountListView,
    DashboardBankAccountUpdateView,
    DashboardSupportContentView,
)
from .views import DashboardIndexView

app_name = "dashboard"

urlpatterns = [
    path("", DashboardIndexView.as_view(), name="index"),

    path("teachings/", DashboardSermonListView.as_view(), name="sermon_list"),
    path("teachings/new/", DashboardSermonCreateView.as_view(), name="sermon_create"),
    path("teachings/<slug:slug>/edit/", DashboardSermonUpdateView.as_view(), name="sermon_update"),
    path("teachings/<slug:slug>/delete/", DashboardSermonDeleteView.as_view(), name="sermon_delete"),

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

    path("gallery/", DashboardGalleryPhotoListView.as_view(), name="gallery_photo_list"),
    path("gallery/new/", DashboardGalleryPhotoCreateView.as_view(), name="gallery_photo_create"),
    path("gallery/<slug:slug>/edit/", DashboardGalleryPhotoUpdateView.as_view(), name="gallery_photo_update"),
    path("gallery/<slug:slug>/delete/", DashboardGalleryPhotoDeleteView.as_view(), name="gallery_photo_delete"),

    path("settings/", DashboardChurchSettingsView.as_view(), name="church_settings"),
    path("settings/seo/", DashboardSEODefaultsView.as_view(), name="seo_defaults"),
    path("settings/notifications/", DashboardNotificationSettingsView.as_view(), name="notification_settings"),

    path("service-times/", DashboardServiceTimeListView.as_view(), name="service_time_list"),
    path("service-times/new/", DashboardServiceTimeCreateView.as_view(), name="service_time_create"),
    path("service-times/<int:pk>/edit/", DashboardServiceTimeUpdateView.as_view(), name="service_time_update"),
    path("service-times/<int:pk>/delete/", DashboardServiceTimeDeleteView.as_view(), name="service_time_delete"),

    path("media/", DashboardMediaLibraryView.as_view(), name="media_library"),
    path("school/", DashboardSchoolInfoView.as_view(), name="school_info"),

    path("support/", DashboardSupportContentView.as_view(), name="support_content"),
    path("support/bank-accounts/", DashboardBankAccountListView.as_view(), name="bank_account_list"),
    path("support/bank-accounts/new/", DashboardBankAccountCreateView.as_view(), name="bank_account_create"),
    path("support/bank-accounts/<int:pk>/edit/", DashboardBankAccountUpdateView.as_view(), name="bank_account_update"),
    path("support/bank-accounts/<int:pk>/delete/", DashboardBankAccountDeleteView.as_view(), name="bank_account_delete"),
]