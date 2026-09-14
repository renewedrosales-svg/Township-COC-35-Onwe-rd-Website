from django.views.generic import ListView

from .models import GalleryPhoto


class GalleryListView(ListView):
    model = GalleryPhoto
    template_name = "gallery/list.html"
    context_object_name = "photos"
    paginate_by = 12

    def get_queryset(self):
        qs = GalleryPhoto.objects.filter(is_published=True).select_related("event")

        query = self.request.GET.get("q", "").strip()
        if query:
            qs = qs.filter(title__icontains=query)

        category = self.request.GET.get("category", "").strip()
        if category:
            qs = qs.filter(category=category)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = GalleryPhoto.CATEGORY_CHOICES
        context["current_category"] = self.request.GET.get("category", "")
        context["current_query"] = self.request.GET.get("q", "")
        return context