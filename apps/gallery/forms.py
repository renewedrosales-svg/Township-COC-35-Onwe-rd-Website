from django import forms

from apps.core.forms import TailwindStyledFormMixin

from .models import GalleryPhoto


class GalleryPhotoForm(TailwindStyledFormMixin, forms.ModelForm):
    class Meta:
        model = GalleryPhoto
        fields = ["title", "image", "category", "alt_text", "event", "photo_date", "is_featured", "is_published", "order"]
        widgets = {
            "photo_date": forms.DateInput(attrs={"type": "date"}),
        }