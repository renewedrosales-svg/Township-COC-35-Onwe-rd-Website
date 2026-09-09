from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.core.audit import log_action
from apps.core.mixins import MinisterOwnershipRequiredMixin, MinisterRequiredMixin
from apps.sermons.forms import SermonForm
from apps.sermons.models import Sermon


def _is_elevated(user):
    return user.groups.filter(name__in=("Church Admin", "Super Admin")).exists()


class DashboardSermonListView(MinisterRequiredMixin, ListView):
    model = Sermon
    template_name = "dashboard/sermons/list.html"
    context_object_name = "sermons"
    paginate_by = 20

    def get_queryset(self):
        qs = Sermon.objects.select_related("speaker", "category").order_by("-date_delivered")
        if _is_elevated(self.request.user):
            return qs
        return qs.filter(created_by=self.request.user)


class DashboardSermonCreateView(MinisterRequiredMixin, CreateView):
    model = Sermon
    form_class = SermonForm
    template_name = "dashboard/sermons/form.html"
    success_url = reverse_lazy("dashboard:sermon_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        log_action(self.request.user, "publish" if self.object.is_published else "create", self.object)
        messages.success(self.request, "Teaching saved.")
        return response


class DashboardSermonUpdateView(MinisterOwnershipRequiredMixin, UpdateView):
    model = Sermon
    form_class = SermonForm
    template_name = "dashboard/sermons/form.html"
    success_url = reverse_lazy("dashboard:sermon_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        # Belt-and-suspenders: the queryset itself is scoped for
        # Ministers too, not just the mixin's test_func. Even if the
        # mixin check were ever bypassed by a future code change,
        # get_object() still physically cannot fetch another
        # minister's sermon from the database.
        qs = Sermon.objects.all()
        if _is_elevated(self.request.user):
            return qs
        return qs.filter(created_by=self.request.user)

    def form_valid(self, form):
        was_published = Sermon.objects.filter(pk=self.object.pk, is_published=True).exists()
        response = super().form_valid(form)
        if self.object.is_published and not was_published:
            action = "publish"
        elif not self.object.is_published and was_published:
            action = "unpublish"
        else:
            action = "update"
        log_action(self.request.user, action, self.object)
        messages.success(self.request, "Teaching updated.")
        return response


class DashboardSermonDeleteView(MinisterOwnershipRequiredMixin, DeleteView):
    model = Sermon
    template_name = "dashboard/sermons/confirm_delete.html"
    success_url = reverse_lazy("dashboard:sermon_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        qs = Sermon.objects.all()
        if _is_elevated(self.request.user):
            return qs
        return qs.filter(created_by=self.request.user)

    def form_valid(self, form):
        log_action(self.request.user, "delete", self.object)
        messages.success(self.request, "Teaching deleted.")
        return super().form_valid(form)