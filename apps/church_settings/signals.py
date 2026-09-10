from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .context_processors import CACHE_KEY_SERVICE_TIMES, CACHE_KEY_SETTINGS
from .models import ChurchSettings, ServiceTime


@receiver(post_save, sender=ChurchSettings)
def clear_settings_cache(sender, **kwargs):
    cache.delete(CACHE_KEY_SETTINGS)


@receiver([post_save, post_delete], sender=ServiceTime)
def clear_service_times_cache(sender, **kwargs):
    cache.delete(CACHE_KEY_SERVICE_TIMES)