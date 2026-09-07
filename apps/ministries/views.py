from django.views.generic import DetailView, ListView

from .models import Ministry


class MinistryListView(ListView):
    model = Ministry
    template_name = "ministries/list.html"
    context_object_name = "ministries"

    def get_queryset(self):
        return Ministry.objects.filter(is_active=True).select_related("leader")


class MinistryDetailView(DetailView):
    model = Ministry
    template_name = "ministries/detail.html"
    context_object_name = "ministry"

    def get_queryset(self):
        return Ministry.objects.filter(is_active=True).select_related("leader")