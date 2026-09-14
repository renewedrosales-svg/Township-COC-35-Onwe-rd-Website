from django.db.models import Count, Q
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
        # annotate() computes each category's PUBLISHED sermon count in
        # one query (not one query per category in a template loop),
        # matching the project's established select_related/no-N+1
        # discipline. Filtered on sermon__is_published so a category
        # with only drafts correctly shows 0, not a misleading count
        # of unpublished content.
        context["categories"] = SermonCategory.objects.annotate(
            sermon_count=Count("sermons", filter=Q(sermons__is_published=True))
        )
        context["total_sermon_count"] = Sermon.objects.filter(is_published=True).count()
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