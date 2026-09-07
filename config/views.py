from django.http import JsonResponse


def health_check(request):
    """Used by Render (and any uptime monitor) to confirm the app is alive."""
    return JsonResponse({"status": "ok"})