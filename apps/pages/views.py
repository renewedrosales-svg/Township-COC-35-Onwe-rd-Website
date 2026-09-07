from django.views.generic import DetailView, TemplateView

from apps.ministries.models import Leader

from .models import AboutPageContent, Page


class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_content = AboutPageContent.load()
        context["about_content"] = about_content
        if about_content.show_leadership_section:
            context["leaders"] = Leader.objects.filter(is_active=True)
        return context


class PageDetailView(DetailView):
    model = Page
    template_name = "pages/page_detail.html"
    context_object_name = "page"

    def get_queryset(self):
        # Draft pages are genuinely unreachable — not merely unlisted in
        # navigation. Guessing or knowing a draft's slug doesn't work.
        return Page.objects.filter(is_published=True)