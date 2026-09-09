from django.contrib import messages
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .audit import log_action
from .mixins import ChurchAdminRequiredMixin

from django.contrib import messages
from django.views.generic.edit import FormView


class DashboardListView(ChurchAdminRequiredMixin, ListView):
    """
    Shared base for every Church Admin+ content list. Subclasses supply
    `model` and their own `template_name` (list layouts genuinely differ
    per content type — this base only centralizes the permission gate
    and pagination default, not the table markup).
    """
    paginate_by = 20


class DashboardCreateView(ChurchAdminRequiredMixin, CreateView):
    """
    Shared base for every Church Admin+ "new record" form. Uses one
    generic template (dashboard/generic/form.html) since a form is
    just "loop over fields" regardless of model — genuinely reusable,
    unlike list views.
    """
    template_name = "dashboard/generic/form.html"

    def form_valid(self, form):
        if hasattr(form.instance, "created_by_id"):
            form.instance.created_by = self.request.user
        response = super().form_valid(form)
        log_action(self.request.user, "create", self.object)
        messages.success(self.request, f"{self.model._meta.verbose_name} saved.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("cancel_url", self.success_url)
        context.setdefault("page_title", f"New {self.model._meta.verbose_name}")
        return context


class DashboardUpdateView(ChurchAdminRequiredMixin, UpdateView):
    template_name = "dashboard/generic/form.html"

    def form_valid(self, form):
        if hasattr(form.instance, "updated_by_id"):
            form.instance.updated_by = self.request.user
        response = super().form_valid(form)
        log_action(self.request.user, "update", self.object)
        messages.success(self.request, f"{self.model._meta.verbose_name} updated.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("cancel_url", self.success_url)
        context.setdefault("page_title", f"Edit {self.model._meta.verbose_name}")
        return context


class DashboardDeleteView(ChurchAdminRequiredMixin, DeleteView):
    template_name = "dashboard/generic/confirm_delete.html"

    def form_valid(self, form):
        log_action(self.request.user, "delete", self.object)
        messages.success(self.request, f"{self.model._meta.verbose_name} deleted.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("cancel_url", self.success_url)
        return context



class DashboardSingletonUpdateView(ChurchAdminRequiredMixin, FormView):
    """
    Shared base for editing any SingletonModel (ChurchSettings, and
    reusable for HomepageContent/AboutPageContent/SupportPageContent
    if we ever move those into the dashboard too — not done today
    since Phases 4/5/6/11 already have them working fine in /admin/,
    and moving them isn't asked for; this exists specifically to
    support Church Settings and SEO Defaults below without writing
    two near-identical singleton-form views by hand.
    """
    template_name = "dashboard/generic/form.html"
    singleton_model = None  # subclasses set this
    page_title = "Settings"

    def get_initial(self):
        return self.singleton_model.load().__dict__

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.singleton_model.load()
        return kwargs

    def form_valid(self, form):
        form.save()
        from .audit import log_action
        log_action(self.request.user, "update", form.instance)
        messages.success(self.request, "Settings saved.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context.setdefault("cancel_url", self.success_url)
        return context