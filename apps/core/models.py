from django.db import models


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