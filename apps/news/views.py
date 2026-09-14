from django.db.models import Count, Q
from django.views.generic import DetailView, ListView

from .models import Article, NewsCategory


class NewsListView(ListView):
    model = Article
    template_name = "news/list.html"
    context_object_name = "articles"
    paginate_by = 9

    def get_queryset(self):
        qs = Article.objects.public().select_related("author", "category")

        query = self.request.GET.get("q", "").strip()
        if query:
            qs = qs.filter(title__icontains=query)

        category_slug = self.request.GET.get("category", "").strip()
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        # Uniform grid now (no large featured-article hero card per the
        # News redesign) — featured articles simply sort first within
        # the normal grid, rather than being pulled out into a special
        # layout slot the way Phase 9 originally built it.
        return qs.order_by("-is_featured", "-publish_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = NewsCategory.objects.annotate(
            article_count=Count(
                "articles",
                filter=Q(articles__status="published", articles__publish_date__lte=self._now()),
            )
        )
        context["total_article_count"] = Article.objects.public().count()
        context["current_category"] = self.request.GET.get("category", "")
        context["current_query"] = self.request.GET.get("q", "")
        context["recent_posts"] = (
            Article.objects.public().select_related("category").order_by("-publish_date")[:5]
        )
        return context

    def _now(self):
        from django.utils import timezone
        return timezone.now()


class NewsDetailView(DetailView):
    model = Article
    template_name = "news/detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return Article.objects.public().select_related("author", "category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_articles"] = (
            Article.objects.public()
            .exclude(pk=self.object.pk)
            .order_by("-publish_date")[:3]
        )
        return context