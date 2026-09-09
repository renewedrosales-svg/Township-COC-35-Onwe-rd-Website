from django.urls import reverse_lazy

from apps.core.dashboard_views import (
    DashboardCreateView,
    DashboardDeleteView,
    DashboardListView,
    DashboardUpdateView,
)
from apps.gallery.forms import GalleryAlbumForm
from apps.gallery.models import GalleryAlbum


class DashboardAlbumListView(DashboardListView):
    model = GalleryAlbum
    template_name = "dashboard/gallery/list.html"
    context_object_name = "albums"

    def get_queryset(self):
        return GalleryAlbum.objects.select_related("event").prefetch_related("images").order_by("order", "-created_at")


class DashboardAlbumCreateView(DashboardCreateView):
    model = GalleryAlbum
    form_class = GalleryAlbumForm
    success_url = reverse_lazy("dashboard:album_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["admin_hint"] = True
        return context


class DashboardAlbumUpdateView(DashboardUpdateView):
    model = GalleryAlbum
    form_class = GalleryAlbumForm
    success_url = reverse_lazy("dashboard:album_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["admin_hint"] = True
        context["admin_edit_url"] = f"/admin/gallery/galleryalbum/{self.object.pk}/change/"
        return context


class DashboardAlbumDeleteView(DashboardDeleteView):
    model = GalleryAlbum
    success_url = reverse_lazy("dashboard:album_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"