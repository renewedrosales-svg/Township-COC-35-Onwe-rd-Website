from django.views.generic import DetailView, ListView

from .models import Article, NewsCategory


class NewsListView(ListView):
    model = Article
    template_name = "news/list.html"
    context_object_name = "articles"
    paginate_by = 9

    def get_queryset(self):
        qs = Article.objects.public().select_related("author", "category")

        category_slug = self.request.GET.get("category", "").strip()
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        # Featured article is handled separately in get_context_data and
        # excluded from the grid here so it isn't shown twice — but only
        # on the unfiltered, first page, matching how a "lead story"
        # naturally stops making sense once you're filtering/paging.
        if not category_slug and self.request.GET.get("page", "1") == "1":
            featured = qs.filter(is_featured=True).first()
            if featured:
                qs = qs.exclude(pk=featured.pk)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = NewsCategory.objects.all()
        context["current_category"] = self.request.GET.get("category", "")

        context["featured_article"] = None
        if not context["current_category"] and self.request.GET.get("page", "1") == "1":
            context["featured_article"] = (
                Article.objects.public().select_related("author", "category")
                .filter(is_featured=True).first()
            )
        return context


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