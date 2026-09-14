from django import forms

from apps.core.forms import TailwindStyledFormMixin

from .models import BankAccount, ContactMessage, Page, SupportPageContent

INPUT_CLASSES = (
    "w-full border border-border rounded-xl px-4 py-3 font-body text-sm "
    "text-navy focus:outline-none focus:ring-2 focus:ring-gold transition-colors"
)


class ContactForm(forms.ModelForm):
    # Honeypot field: real users never see or fill this (hidden via
    # CSS in the template, not `type="hidden"`, since some bots skip
    # genuinely hidden inputs but still fill visually-hidden ones).
    # Any value here means it's a bot — reject silently rather than
    # telling the bot exactly why it was blocked.
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={"autocomplete": "off"}))

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Your full name"}),
            "email": forms.EmailInput(attrs={"class": INPUT_CLASSES, "placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Optional"}),
            "subject": forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "What's this about?"}),
            "message": forms.Textarea(attrs={"class": INPUT_CLASSES, "rows": 5, "placeholder": "Write your message here..."}),
        }

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Spam detected.")  # message never actually shown to a real user
        return value


class PageForm(TailwindStyledFormMixin, forms.ModelForm):
    class Meta:
        model = Page
        fields = ["title", "slug", "body", "seo_title", "seo_description", "is_published"]
        widgets = {"body": forms.Textarea(attrs={"rows": 10})}


class BankAccountForm(TailwindStyledFormMixin, forms.ModelForm):
    class Meta:
        model = BankAccount
        # support_content deliberately excluded — auto-assigned in the
        # dashboard create view, since there's only ever one
        # SupportPageContent row (SingletonModel) for it to attach to.
        fields = ["label", "bank_name", "account_name", "account_number", "additional_info", "order", "is_active"]


class SupportPageContentForm(TailwindStyledFormMixin, forms.ModelForm):
    class Meta:
        model = SupportPageContent
        fields = ["heading", "intro_text"]
        widgets = {"intro_text": forms.Textarea(attrs={"rows": 4})}