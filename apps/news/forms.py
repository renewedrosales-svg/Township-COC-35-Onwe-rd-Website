from django import forms

from apps.core.forms import TailwindStyledFormMixin

from .models import Article


class ArticleForm(TailwindStyledFormMixin, forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title", "slug", "excerpt", "body", "featured_image",
            "author", "category", "status", "publish_date",
            "is_featured", "seo_title", "seo_description",
        ]
        widgets = {
            "excerpt": forms.Textarea(attrs={"rows": 2}),
            "body": forms.Textarea(attrs={"rows": 10}),
            "publish_date": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # DateTimeInput needs the initial value formatted to match the
        # HTML datetime-local input's expected format, or Django's
        # default rendering won't populate the field correctly when
        # editing an existing article with a publish_date already set.
        self.fields["publish_date"].input_formats = ["%Y-%m-%dT%H:%M"]