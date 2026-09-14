from django.views.generic import DetailView, ListView

from .models import Ministry


class MinistryListView(ListView):
    model = Ministry
    template_name = "ministries/list.html"
    context_object_name = "ministries"
    paginate_by = 9

    def get_queryset(self):
        qs = Ministry.objects.filter(is_active=True).select_related("leader")

        query = self.request.GET.get("q", "").strip()
        if query:
            qs = qs.filter(name__icontains=query)

        return qs.order_by("-is_featured", "order", "name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_query"] = self.request.GET.get("q", "")
        context["total_ministry_count"] = Ministry.objects.filter(is_active=True).count()
        return context


class MinistryDetailView(DetailView):
    model = Ministry
    template_name = "ministries/detail.html"
    context_object_name = "ministry"

    def get_queryset(self):
        return Ministry.objects.filter(is_active=True).select_related("leader")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["other_ministries"] = (
            Ministry.objects.filter(is_active=True)
            .exclude(pk=self.object.pk)
            .select_related("leader")
            .order_by("-is_featured", "order", "name")[:3]
        )
        return context