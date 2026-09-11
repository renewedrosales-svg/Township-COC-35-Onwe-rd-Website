from django.contrib.auth import views as auth_views

from .auth_throttle import get_client_ip, is_locked_out


class RateLimitAwareLoginView(auth_views.LoginView):
    """
    Wraps Django's LoginView to return a genuine HTTP 429 when the
    Phase 15 login throttle has locked out this username+IP, instead
    of a normal 200 with a form validation error. The form itself
    (StyledLoginForm) still does the actual lockout CHECK and records
    failures — this view only intercepts to set the correct status
    code before rendering.
    """

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        ip = get_client_ip(request)
        if username and is_locked_out(username, ip):
            from apps.core.views import render_429
            return render_429(
                request,
                "Too many failed login attempts. Please wait 15 minutes and try again.",
            )
        return super().post(request, *args, **kwargs)