from django.template.response import TemplateResponse

from django.http import HttpResponse
from django.template import loader

def robots_txt(request):
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    return TemplateResponse(
        request, "robots.txt", {"sitemap_url": sitemap_url}, content_type="text/plain",
    )


def custom_400(request, exception=None):
    template = loader.get_template("errors/400.html")
    return HttpResponse(template.render({}, request), status=400)


def custom_403(request, exception=None):
    template = loader.get_template("errors/403.html")
    return HttpResponse(template.render({}, request), status=403)


def custom_404(request, exception=None):
    template = loader.get_template("errors/404.html")
    return HttpResponse(template.render({}, request), status=404)


def custom_500(request):
    # Deliberately does NOT use loader.get_template + context processors
    # the normal way other error views do — a 500 can be caused by a
    # database outage, and church_context (used by base.html sitewide)
    # queries the database. Rendering this the normal way could throw
    # a second exception while trying to display the first one. This
    # template is standalone HTML with zero DB dependency — see the
    # template itself.
    template = loader.get_template("errors/500.html")
    return HttpResponse(template.render({}, request), status=500)


def render_429(request, message="Too many requests. Please wait a few minutes and try again."):
    """
    Not a Django error-handler hook (no handler429 exists in Django,
    unlike 400/403/404/500) — this is a plain helper called directly
    from the two places in the project that actually rate-limit
    requests: the contact form (Phase 11) and the login throttle
    (Phase 15 Step 1). Import and call this instead of returning a
    normal 200 with a messages-framework error, so a genuinely
    rate-limited request gets the semantically correct HTTP status.
    """
    template = loader.get_template("errors/429.html")
    context = {"rate_limit_message": message}
    return HttpResponse(template.render(context, request), status=429)