from .models import AuditLog


def log_action(user, action, obj):
    """
    Call from an admin's save_model/delete_model, or a dashboard view,
    right after the actual save/delete succeeds.

    Usage: log_action(request.user, "create", page_instance)
    """
    AuditLog.objects.create(
        user=user if getattr(user, "is_authenticated", False) else None,
        action=action,
        model_name=obj.__class__.__name__,
        object_repr=str(obj)[:255],
        object_id=str(obj.pk),
    )