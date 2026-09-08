from django.views.generic import DetailView, ListView

from .models import GalleryAlbum


class GalleryAlbumListView(ListView):
    model = GalleryAlbum
    template_name = "gallery/list.html"
    context_object_name = "albums"
    paginate_by = 12

    def get_queryset(self):
        return (
            GalleryAlbum.objects.filter(is_published=True)
            .prefetch_related("images")
            .select_related("event")
        )


class GalleryAlbumDetailView(DetailView):
    model = GalleryAlbum
    template_name = "gallery/detail.html"
    context_object_name = "album"

    def get_queryset(self):
        return (
            GalleryAlbum.objects.filter(is_published=True)
            .prefetch_related("images")
            .select_related("event")
        )