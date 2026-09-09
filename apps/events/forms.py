from django import forms

from apps.core.forms import TailwindStyledFormMixin

from .models import Event


class EventForm(TailwindStyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title", "description", "event_date", "start_time", "end_time",
            "location", "image", "organizer", "registration_info",
            "external_link", "is_featured", "is_published",
        ]
        widgets = {
            "event_date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
            "description": forms.Textarea(attrs={"rows": 5}),
            "registration_info": forms.Textarea(attrs={"rows": 3}),
        }