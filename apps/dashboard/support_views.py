from django.urls import reverse_lazy

from apps.core.dashboard_views import (
    DashboardCreateView,
    DashboardDeleteView,
    DashboardListView,
    DashboardSingletonUpdateView,
    DashboardUpdateView,
)
from apps.core.mixins import SuperAdminRequiredMixin
from apps.pages.forms import BankAccountForm, SupportPageContentForm
from apps.pages.models import BankAccount, SupportPageContent


class DashboardSupportContentView(SuperAdminRequiredMixin, DashboardSingletonUpdateView):
    singleton_model = SupportPageContent
    form_class = SupportPageContentForm
    success_url = reverse_lazy("dashboard:support_content")
    page_title = "Support Page Content"


class DashboardBankAccountListView(SuperAdminRequiredMixin, DashboardListView):
    model = BankAccount
    template_name = "dashboard/support/bank_account_list.html"
    context_object_name = "bank_accounts"

    def get_queryset(self):
        return BankAccount.objects.order_by("order", "label")


class DashboardBankAccountCreateView(SuperAdminRequiredMixin, DashboardCreateView):
    model = BankAccount
    form_class = BankAccountForm
    success_url = reverse_lazy("dashboard:bank_account_list")

    def form_valid(self, form):
        form.instance.support_content = SupportPageContent.load()
        return super().form_valid(form)


class DashboardBankAccountUpdateView(SuperAdminRequiredMixin, DashboardUpdateView):
    model = BankAccount
    form_class = BankAccountForm
    success_url = reverse_lazy("dashboard:bank_account_list")


class DashboardBankAccountDeleteView(SuperAdminRequiredMixin, DashboardDeleteView):
    model = BankAccount
    success_url = reverse_lazy("dashboard:bank_account_list")