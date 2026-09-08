from django.contrib import admin

from apps.core.audit import log_action

from .models import Article, NewsCategory


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "publish_date", "is_featured")
    list_filter = ("status", "is_featured", "category")
    list_editable = ("status", "is_featured")
    search_fields = ("title", "body", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish_date"

    fieldsets = (
        (None, {"fields": ("title", "slug", "excerpt", "body", "featured_image")}),
        ("Attribution & Category", {"fields": ("author", "category")}),
        ("Publishing", {"fields": ("status", "publish_date", "is_featured")}),
        ("SEO", {"fields": ("seo_title", "seo_description")}),
    )

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        if not change:
            obj.created_by = request.user
        was_published = False
        if change:
            was_published = Article.objects.filter(pk=obj.pk, status=Article.Status.PUBLISHED).exists()
        super().save_model(request, obj, form, change)

        if not change:
            action = "create"
        elif obj.status == Article.Status.PUBLISHED and not was_published:
            action = "publish"
        elif obj.status != Article.Status.PUBLISHED and was_published:
            action = "unpublish"
        else:
            action = "update"
        log_action(request.user, action, obj)

    def delete_model(self, request, obj):
        log_action(request.user, "delete", obj)
        super().delete_model(request, obj)