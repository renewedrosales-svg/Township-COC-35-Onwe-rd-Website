from django import forms

from apps.core.forms import TailwindStyledFormMixin

from .models import SchoolInfo


class SchoolInfoForm(TailwindStyledFormMixin, forms.ModelForm):
    class Meta:
        model = SchoolInfo
        fields = ["school_name", "intro_text", "hero_image", "about_preview", "programs_preview", "contact_email", "contact_phone"]
        widgets = {
            "intro_text": forms.Textarea(attrs={"rows": 3}),
            "about_preview": forms.Textarea(attrs={"rows": 4}),
            "programs_preview": forms.Textarea(attrs={"rows": 4}),
        }