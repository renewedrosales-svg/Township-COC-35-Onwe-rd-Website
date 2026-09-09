from django.views.generic import TemplateView

from apps.core.mixins import ChurchAdminRequiredMixin, MinisterRequiredMixin
from apps.core.models import AuditLog
from apps.events.models import Event
from apps.news.models import Article
from apps.sermons.models import Sermon


class DashboardIndexView(MinisterRequiredMixin, TemplateView):
    """
    Overview lands everyone who can reach the dashboard at all
    (Minister and above) on a real page — but the STATS shown are
    scoped by role, so a Minister sees relevant numbers about their
    own content, not sitewide admin metrics they have no reason to see.
    """
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_church_admin = user.groups.filter(name__in=("Church Admin", "Super Admin")).exists()

        if is_church_admin:
            context["stats"] = {
                "published_sermons": Sermon.objects.filter(is_published=True).count(),
                "draft_sermons": Sermon.objects.filter(is_published=False).count(),
                "upcoming_events": Event.objects.filter(is_published=True).count(),
                "published_articles": Article.objects.public().count(),
            }
            context["recent_activity"] = AuditLog.objects.select_related("user")[:10]
        else:
            # Minister sees only their own content's numbers.
            my_sermons = Sermon.objects.filter(created_by=user)
            context["stats"] = {
                "my_published_sermons": my_sermons.filter(is_published=True).count(),
                "my_draft_sermons": my_sermons.filter(is_published=False).count(),
            }
            context["recent_activity"] = None

        context["is_church_admin"] = is_church_admin
        return context