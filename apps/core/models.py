from django.db import models
from django.conf import settings


class SingletonModel(models.Model):
    """
    Abstract base for models that must only ever have exactly one row
    (e.g. ChurchSettings). Forces every save to overwrite the same
    primary key (1), and provides `load()` to fetch-or-create that row
    safely from anywhere in the project — views, templates, shell.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # singleton rows are never deletable — settings must always exist

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj


class AuditLog(models.Model):
    """
    Records administrative actions on sensitive content, per §40.
    Written via `log_action()` below — called from admin save_model/
    delete_model hooks now, and from custom dashboard views once
    Phase 12 replaces raw Django admin as the primary CMS surface.

    Deliberately does NOT store request bodies, form data, or secrets —
    only who did what to which object, and when.
    """
    ACTION_CHOICES = [
        ("create", "Created"),
        ("update", "Updated"),
        ("delete", "Deleted"),
        ("publish", "Published"),
        ("unpublish", "Unpublished"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_repr = models.CharField(max_length=255)
    object_id = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Audit Log Entry"
        verbose_name_plural = "Audit Log Entries"

    def __str__(self):
        return f"{self.user} {self.action} {self.model_name} #{self.object_id}"