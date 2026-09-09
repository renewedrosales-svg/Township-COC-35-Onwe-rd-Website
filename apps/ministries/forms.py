from django import forms

from apps.core.forms import TailwindStyledFormMixin

from .models import Leader, Ministry


class MinistryForm(TailwindStyledFormMixin, forms.ModelForm):
    class Meta:
        model = Ministry
        fields = [
            "name", "description", "image", "leader", "meeting_info",
            "contact_email", "contact_phone", "is_featured", "is_active", "order",
        ]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}


class LeaderForm(TailwindStyledFormMixin, forms.ModelForm):
    class Meta:
        model = Leader
        fields = [
            "user", "full_name", "position_title", "photo", "bio",
            "public_email", "facebook_url", "instagram_url",
            "display_order", "is_active",
        ]
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}