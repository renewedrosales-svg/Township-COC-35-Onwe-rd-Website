from django.contrib import admin

from apps.core.audit import log_action

from .models import AboutPageContent, Page

from .models import AboutPageContent, BankAccount, ContactMessage, Page, SupportPageContent


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "updated_at")
    list_filter = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        log_action(request.user, "update" if change else "create", obj)

    def delete_model(self, request, obj):
        log_action(request.user, "delete", obj)
        super().delete_model(request, obj)


@admin.register(AboutPageContent)
class AboutPageContentAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Hero", {"fields": ("hero_image",)}),
        ("Content", {"fields": ("who_we_are", "our_history", "our_mission", "our_vision", "our_values", "statement_of_faith")}),
        ("Leadership Display", {"fields": ("show_leadership_section",)}),
    )

    def has_add_permission(self, request):
        return not AboutPageContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        log_action(request.user, "update", obj)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read",)
    list_editable = ("is_read",)
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "phone", "subject", "message", "submitted_ip", "created_at")

    def has_add_permission(self, request):
        return False  # only ever created via the public form, never fabricated in admin


class BankAccountInline(admin.TabularInline):
    model = BankAccount
    extra = 1


@admin.register(SupportPageContent)
class SupportPageContentAdmin(admin.ModelAdmin):
    fields = ("heading", "intro_text")
    inlines = [BankAccountInline]

    def has_add_permission(self, request):
        return not SupportPageContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        log_action(request.user, "update", obj)