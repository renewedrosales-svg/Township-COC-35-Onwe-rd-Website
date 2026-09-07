from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(*allowed_groups):
    """
    Function-based view equivalent of RoleRequiredMixin.

    Usage:
        @role_required("Church Admin", "Super Admin")
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not request.user.groups.filter(name__in=allowed_groups).exists():
                raise PermissionDenied(
                    "You don't have permission to access this area of the dashboard."
                )
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator