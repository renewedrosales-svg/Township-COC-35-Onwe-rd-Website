from django.contrib import admin

from apps.core.audit import log_action

from .models import Sermon, SermonCategory


@admin.register(SermonCategory)
class SermonCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ("title", "speaker", "date_delivered", "category", "is_featured", "is_published")
    list_filter = ("is_published", "is_featured", "category")
    list_editable = ("is_featured", "is_published")
    search_fields = ("title", "scripture_reference")
    prepopulated_fields = {"slug": ("title",)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Ministers only ever see (and can therefore only ever act on,
        # even via admin's own permission checks) their own sermons.
        # Church Admin / Super Admin see everything.
        if request.user.groups.filter(name__in=("Church Admin", "Super Admin")).exists():
            return qs
        return qs.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        log_action(request.user, "publish" if obj.is_published else ("update" if change else "create"), obj)

    def delete_model(self, request, obj):
        log_action(request.user, "delete", obj)
        super().delete_model(request, obj)