from django.urls import reverse_lazy

from apps.core.dashboard_views import (
    DashboardCreateView,
    DashboardDeleteView,
    DashboardListView,
    DashboardUpdateView,
)
from apps.gallery.forms import GalleryPhotoForm
from apps.gallery.models import GalleryPhoto


class DashboardGalleryPhotoListView(DashboardListView):
    model = GalleryPhoto
    template_name = "dashboard/gallery/list.html"
    context_object_name = "photos"

    def get_queryset(self):
        return GalleryPhoto.objects.order_by("order", "-photo_date")


class DashboardGalleryPhotoCreateView(DashboardCreateView):
    model = GalleryPhoto
    form_class = GalleryPhotoForm
    success_url = reverse_lazy("dashboard:gallery_photo_list")


class DashboardGalleryPhotoUpdateView(DashboardUpdateView):
    model = GalleryPhoto
    form_class = GalleryPhotoForm
    success_url = reverse_lazy("dashboard:gallery_photo_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"


class DashboardGalleryPhotoDeleteView(DashboardDeleteView):
    model = GalleryPhoto
    success_url = reverse_lazy("dashboard:gallery_photo_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"