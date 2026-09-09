from django.urls import reverse_lazy

from apps.core.dashboard_views import DashboardSingletonUpdateView
from apps.school.forms import SchoolInfoForm
from apps.school.models import SchoolInfo


class DashboardSchoolInfoView(DashboardSingletonUpdateView):
    singleton_model = SchoolInfo
    form_class = SchoolInfoForm
    success_url = reverse_lazy("dashboard:school_info")
    page_title = "School Info"