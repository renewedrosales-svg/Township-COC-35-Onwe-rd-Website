from django.urls import reverse_lazy

from apps.core.dashboard_views import (
    DashboardCreateView,
    DashboardDeleteView,
    DashboardListView,
    DashboardUpdateView,
)
from apps.news.forms import ArticleForm
from apps.news.models import Article


class DashboardArticleListView(DashboardListView):
    model = Article
    template_name = "dashboard/news/list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.select_related("category").order_by("-publish_date")

    def get_context_data(self, **kwargs):
        from django.utils import timezone
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class DashboardArticleCreateView(DashboardCreateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("dashboard:article_list")


class DashboardArticleUpdateView(DashboardUpdateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("dashboard:article_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def form_valid(self, form):
        from django.contrib import messages
        from django.views.generic.edit import ModelFormMixin

        from apps.core.audit import log_action

        was_published = Article.objects.filter(
            pk=self.object.pk, status=Article.Status.PUBLISHED
        ).exists()

        # Bypass DashboardUpdateView.form_valid (which would log a
        # plain "update") and call straight through to Django's
        # ModelFormMixin instead, so exactly ONE audit entry is
        # written, with the correct, specific action.
        response = ModelFormMixin.form_valid(self, form)

        if self.object.status == Article.Status.PUBLISHED and not was_published:
            action = "publish"
        elif self.object.status != Article.Status.PUBLISHED and was_published:
            action = "unpublish"
        else:
            action = "update"
        log_action(self.request.user, action, self.object)
        messages.success(self.request, "Article updated.")
        return response


class DashboardArticleDeleteView(DashboardDeleteView):
    model = Article
    success_url = reverse_lazy("dashboard:article_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"