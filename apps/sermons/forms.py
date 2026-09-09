from django import forms

from apps.core.forms import TailwindStyledFormMixin

from .models import Sermon


class SermonForm(TailwindStyledFormMixin, forms.ModelForm):
    class Meta:
        model = Sermon
        fields = [
            "title", "speaker", "date_delivered", "scripture_reference",
            "description", "category", "thumbnail", "audio_file",
            "video_url", "notes_pdf", "is_featured", "is_published",
        ]
        widgets = {
            "date_delivered": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 5}),
        }