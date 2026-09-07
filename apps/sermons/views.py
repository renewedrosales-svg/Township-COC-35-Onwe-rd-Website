from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView

from .models import Sermon, SermonCategory


class TeachingListView(ListView):
    model = Sermon
    template_name = "sermons/list.html"
    context_object_name = "sermons"
    paginate_by = 9

    def get_queryset(self):
        qs = Sermon.objects.filter(is_published=True).select_related("speaker", "category")

        query = self.request.GET.get("q", "").strip()
        if query:
            from django.db.models import Q
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(scripture_reference__icontains=query)
                | Q(description__icontains=query)
            )

        category_slug = self.request.GET.get("category", "").strip()
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = SermonCategory.objects.all()
        context["current_query"] = self.request.GET.get("q", "")
        context["current_category"] = self.request.GET.get("category", "")
        return context


class TeachingDetailView(DetailView):
    model = Sermon
    template_name = "sermons/detail.html"
    context_object_name = "sermon"

    def get_queryset(self):
        return Sermon.objects.filter(is_published=True).select_related("speaker", "category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_sermons"] = (
            Sermon.objects.filter(is_published=True)
            .exclude(pk=self.object.pk)
            .order_by("-date_delivered")[:3]
        )
        return context