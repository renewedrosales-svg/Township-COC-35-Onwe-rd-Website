from django.urls import reverse


def build_dashboard_nav(request):
    """
    Returns the sidebar structure for the current user, filtered by
    their actual group membership — mirrors §25's proposed nav
    structure. Each section only appears if the user has at least one
    visible item in it. `active` is set by matching the current path,
    so highlighting the current section requires zero per-view code.

    As each dashboard section is built in later steps of this phase,
    add its entry here — this is the single place the sidebar is
    defined, not per-template.
    """
    user = request.user
    is_super = user.groups.filter(name="Super Admin").exists()
    is_church_admin = is_super or user.groups.filter(name="Church Admin").exists()
    is_minister = is_church_admin or user.groups.filter(name="Minister").exists()
    path = request.path

    def item(label, url_name, *url_args):
        url = reverse(url_name, args=url_args) if url_args else reverse(url_name)
        return {"label": label, "url": url, "active": path.startswith(url)}

    sections = []

    sections.append({
        "label": "Overview",
        "items": [item("Dashboard", "dashboard:index")],
    })
    
    if is_minister:
        content_items = [item("My Teachings", "dashboard:sermon_list")]
        sections.append({"label": "My Content", "items": content_items})

    if is_church_admin:
        sections.append({
            "label": "Church Content",
            "items": [
                item("Pages", "dashboard:page_list"),
                item("Ministries", "dashboard:ministry_list"),
                item("Leadership", "dashboard:leader_list"),
                item("Events", "dashboard:event_list"),
                item("News", "dashboard:article_list"),
                item("Gallery", "dashboard:album_list"),
            ],
        })
    if is_church_admin:
        sections.append({
            "label": "Site Settings",
            "items": [
                item("Media Library", "dashboard:media_library"),
                item("Church Settings", "dashboard:church_settings"),
                item("Service Times", "dashboard:service_time_list"),
                item("SEO Defaults", "dashboard:seo_defaults"),
                item("School Info", "dashboard:school_info"),
            ],
        })

    if is_super:
        sections.append({
            "label": "System",
            "items": [
                {"label": "Django Admin", "url": "/admin/", "active": False},
            ],
        })

    return sections