from django import forms

from .models import ContactMessage


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
            "name": forms.TextInput(attrs={
                "class": "w-full border border-navy/20 rounded-lg px-4 py-2.5 font-body text-sm focus:outline-none focus:ring-2 focus:ring-gold",
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full border border-navy/20 rounded-lg px-4 py-2.5 font-body text-sm focus:outline-none focus:ring-2 focus:ring-gold",
            }),
            "phone": forms.TextInput(attrs={
                "class": "w-full border border-navy/20 rounded-lg px-4 py-2.5 font-body text-sm focus:outline-none focus:ring-2 focus:ring-gold",
            }),
            "subject": forms.TextInput(attrs={
                "class": "w-full border border-navy/20 rounded-lg px-4 py-2.5 font-body text-sm focus:outline-none focus:ring-2 focus:ring-gold",
            }),
            "message": forms.Textarea(attrs={
                "rows": 5,
                "class": "w-full border border-navy/20 rounded-lg px-4 py-2.5 font-body text-sm focus:outline-none focus:ring-2 focus:ring-gold",
            }),
        }

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Spam detected.")  # message never actually shown to a real user
        return value