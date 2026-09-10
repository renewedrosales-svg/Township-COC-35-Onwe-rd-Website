import json

from django.core.cache import cache

from .models import ChurchSettings, ServiceTime

CACHE_KEY_SETTINGS = "church_settings_singleton"
CACHE_KEY_SERVICE_TIMES = "active_service_times"
CACHE_TIMEOUT = 60 * 15  # 15 minutes — long enough to matter, short enough that an edit shows up quickly even without the signal-based invalidation below


def church_context(request):
    church_settings = cache.get(CACHE_KEY_SETTINGS)
    if church_settings is None:
        church_settings = ChurchSettings.load()
        cache.set(CACHE_KEY_SETTINGS, church_settings, CACHE_TIMEOUT)

    service_times = cache.get(CACHE_KEY_SERVICE_TIMES)
    if service_times is None:
        service_times = list(ServiceTime.objects.filter(is_active=True))
        cache.set(CACHE_KEY_SERVICE_TIMES, service_times, CACHE_TIMEOUT)

    structured_data = {
        "@context": "https://schema.org",
        "@type": "Church",
        "name": church_settings.church_name,
        "url": request.build_absolute_uri("/"),
    }
    if church_settings.address:
        structured_data["address"] = church_settings.address
    if church_settings.phone_primary:
        structured_data["telephone"] = church_settings.phone_primary
    if church_settings.logo:
        structured_data["logo"] = request.build_absolute_uri(church_settings.logo.url)

    return {
        "church_settings": church_settings,
        "active_service_times": service_times,
        "nav_links": [
            ("pages:about", "About Us"),
            ("ministries:list", "Ministries"),
            ("sermons:list", "Teachings"),
            ("events:list", "Events"),
            ("news:list", "News"),
            ("gallery:list", "Gallery"),
            ("pages:contact", "Contact"),
            ("school:index", "School"),
        ],
        "church_structured_data": json.dumps(structured_data),
    }