from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Base mixin: require login AND membership in at least one of
    `allowed_groups`. Subclasses set `allowed_groups`.

    Unauthenticated users -> redirected to login (via LoginRequiredMixin).
    Authenticated but wrong role -> raises PermissionDenied (403),
    NOT a silent redirect — the user should know access was refused,
    not wonder why a link quietly did nothing.
    """
    allowed_groups = ()

    def test_func(self):
        return self.request.user.groups.filter(name__in=self.allowed_groups).exists()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied(
            "You don't have permission to access this area of the dashboard."
        )


class SuperAdminRequiredMixin(RoleRequiredMixin):
    """Restricts a view to Super Admin only — system-level operations."""
    allowed_groups = ("Super Admin",)


class ChurchAdminRequiredMixin(RoleRequiredMixin):
    """
    Restricts a view to Church Admin OR Super Admin — day-to-day content
    management. Super Admin is included because a higher role should
    always be able to do what a lower role can, per §7/§9.
    """
    allowed_groups = ("Church Admin", "Super Admin")


class MinisterRequiredMixin(RoleRequiredMixin):
    """
    Restricts a view to any of the three roles — used for views ministers
    need (e.g. their own sermon list), which Church Admin/Super Admin
    should also be able to reach.
    """
    allowed_groups = ("Minister", "Church Admin", "Super Admin")


class OwnerOrElevatedRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Object-level ownership check, layered on TOP of a role mixin (used
    together on update/delete views for owned content like sermons).

    A Minister may only act on objects where `object.created_by == user`.
    Church Admin and Super Admin bypass the ownership check entirely —
    this is the "own sermons only" rule from §8, enforced here rather
    than through Django's group/permission system, which can't express
    per-object ownership.

    Requires the view to define `get_object()` (standard for
    UpdateView/DeleteView/DetailView) and the model to have a
    `created_by` field.
    """

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name__in=("Church Admin", "Super Admin")).exists():
            return True
        obj = self.get_object()
        return getattr(obj, "created_by_id", None) == user.id

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied("You can only manage content you created.")