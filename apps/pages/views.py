from django.views.generic import DetailView, TemplateView

from apps.ministries.models import Leader

from .models import AboutPageContent, Page, SupportPageContent

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from apps.core.audit import log_action
from apps.core.spam_protection import is_rate_limited

from .forms import ContactForm

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


class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("pages:contact")

    def get_client_ip(self):
        forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return self.request.META.get("REMOTE_ADDR")

    def form_valid(self, form):
        if is_rate_limited(self.request):
            messages.error(
                self.request,
                "You've submitted a few messages recently. Please wait a few minutes before trying again.",
            )
            return redirect(self.success_url)

        contact_message = form.save(commit=False)
        contact_message.submitted_ip = self.get_client_ip()
        contact_message.save()

        log_action(self.request.user, "create", contact_message)

        self._send_notification_email(contact_message)

        messages.success(
            self.request,
            "Thank you for reaching out — we've received your message and will get back to you soon.",
        )
        return redirect(self.success_url)

    def form_invalid(self, form):
        # Honeypot failure lands here too (clean_website raises
        # ValidationError) — deliberately shown as a generic error,
        # never revealing that a bot check specifically failed.
        messages.error(self.request, "Please check the form and try again.")
        return super().form_invalid(form)

    def _send_notification_email(self, contact_message):
        from django.conf import settings

        if not settings.CONTACT_FORM_NOTIFY_EMAIL:
            return  # not configured yet — message is still safely stored either way

        try:
            send_mail(
                subject=f"New Contact Form Message: {contact_message.subject or 'No subject'}",
                message=(
                    f"From: {contact_message.name} <{contact_message.email}>\n"
                    f"Phone: {contact_message.phone or 'Not provided'}\n\n"
                    f"{contact_message.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_FORM_NOTIFY_EMAIL],
                fail_silently=True,
            )
        except Exception:
            # Email delivery failing must NEVER lose the submission —
            # it's already safely saved to the database above. This is
            # exactly the resilience §58/§21 calls for: email is a
            # notification convenience, not the system of record.
            pass

class SupportView(TemplateView):
    template_name = "pages/support.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        support_content = SupportPageContent.load()
        context["support_content"] = support_content
        context["bank_accounts"] = support_content.bank_accounts.filter(is_active=True)
        return context