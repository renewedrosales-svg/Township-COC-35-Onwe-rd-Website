from apps.core.dashboard_nav import build_dashboard_nav


def dashboard_context(request):
    """
    Only builds nav data for authenticated users under /dashboard/ —
    cheap no-op for every public-site request, avoiding wasted queries
    on every page load project-wide.
    """
    if request.path.startswith("/dashboard/") and request.user.is_authenticated:
        return {"dashboard_nav": build_dashboard_nav(request)}
    return {}