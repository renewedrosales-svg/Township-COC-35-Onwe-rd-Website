from django.contrib import admin

from apps.core.audit import log_action

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_date", "start_time", "location", "is_featured", "is_published")
    list_filter = ("is_published", "is_featured")
    list_editable = ("is_featured", "is_published")
    search_fields = ("title", "location", "organizer")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "event_date"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        log_action(request.user, "update" if change else "create", obj)

    def delete_model(self, request, obj):
        log_action(request.user, "delete", obj)
        super().delete_model(request, obj)