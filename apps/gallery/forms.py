from django import forms

from apps.core.forms import TailwindStyledFormMixin

from .models import GalleryAlbum


class GalleryAlbumForm(TailwindStyledFormMixin, forms.ModelForm):
    class Meta:
        model = GalleryAlbum
        fields = ["title", "description", "event", "is_published", "order"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}