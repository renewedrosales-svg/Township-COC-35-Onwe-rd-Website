from django.template.response import TemplateResponse


def robots_txt(request):
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    return TemplateResponse(
        request, "robots.txt", {"sitemap_url": sitemap_url}, content_type="text/plain",
    )