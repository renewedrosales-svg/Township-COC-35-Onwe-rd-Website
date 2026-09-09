from .models import ChurchSettings, ServiceTime


def church_context(request):
    """
    Makes `church_settings` and `active_service_times` available in every
    template project-wide, without any view needing to fetch them manually.
    Registered in TEMPLATES.OPTIONS.context_processors (see settings).
    """
    return {
        "church_settings": ChurchSettings.load(),
        "active_service_times": ServiceTime.objects.filter(is_active=True),
    }


def church_context(request):
    return {
        "church_settings": ChurchSettings.load(),
        "active_service_times": ServiceTime.objects.filter(is_active=True),
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
    }