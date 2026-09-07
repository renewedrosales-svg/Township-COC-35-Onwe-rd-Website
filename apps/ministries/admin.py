from django.contrib import admin

from apps.core.audit import log_action

from .models import Leader, Ministry


@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position_title", "display_order", "is_active")
    list_editable = ("display_order", "is_active")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        log_action(request.user, "update" if change else "create", obj)

    def delete_model(self, request, obj):
        log_action(request.user, "delete", obj)
        super().delete_model(request, obj)


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ("name", "leader", "is_featured", "is_active", "order")
    list_editable = ("is_featured", "is_active", "order")
    list_filter = ("is_active", "is_featured")
    prepopulated_fields = {"slug": ("name",)}

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        log_action(request.user, "update" if change else "create", obj)

    def delete_model(self, request, obj):
        log_action(request.user, "delete", obj)
        super().delete_model(request, obj)