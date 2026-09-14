from django.contrib import admin

from apps.core.audit import log_action

from .models import GalleryPhoto


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "photo_date", "is_featured", "is_published", "order")
    list_filter = ("category", "is_published", "is_featured")
    list_editable = ("is_featured", "is_published", "order")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "photo_date"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        log_action(request.user, "update" if change else "create", obj)

    def delete_model(self, request, obj):
        log_action(request.user, "delete", obj)
        super().delete_model(request, obj)