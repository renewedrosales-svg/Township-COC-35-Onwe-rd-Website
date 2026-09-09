from django.db import models

from apps.core.models import SingletonModel
from apps.core.validators import validate_image_file


def school_upload_path(instance, filename):
    return f"school/{filename}"


class SchoolInfo(SingletonModel):
    school_name = models.CharField(max_length=200, blank=True, default="Church School")
    intro_text = models.TextField(blank=True)
    hero_image = models.ImageField(
        upload_to=school_upload_path, blank=True, null=True,
        validators=[validate_image_file],
    )
    about_preview = models.TextField(
        blank=True, help_text="Short paragraph about the school shown on this page.",
    )
    programs_preview = models.TextField(
        blank=True, help_text="Short overview of programs/classes offered.",
    )
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "School Info"
        verbose_name_plural = "School Info"

    def __str__(self):
        return self.school_name