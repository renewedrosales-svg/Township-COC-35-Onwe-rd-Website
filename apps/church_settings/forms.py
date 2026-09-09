from django import forms

from apps.core.forms import TailwindStyledFormMixin

from .models import ChurchSettings, ServiceTime


class ChurchSettingsForm(TailwindStyledFormMixin, forms.ModelForm):
    class Meta:
        model = ChurchSettings
        fields = [
            "church_name", "tagline", "logo", "favicon",
            "address", "phone_primary", "phone_secondary", "email",
            "facebook_url", "instagram_url", "youtube_url",
            "whatsapp_url", "x_url", "tiktok_url",
            "map_embed_url", "footer_short_description",
        ]


class SEODefaultsForm(TailwindStyledFormMixin, forms.ModelForm):
    class Meta:
        model = ChurchSettings
        fields = ["default_seo_title", "default_seo_description", "default_og_image"]


class ServiceTimeForm(TailwindStyledFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceTime
        fields = ["name", "day", "start_time", "end_time", "location", "description", "is_active", "order"]
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }