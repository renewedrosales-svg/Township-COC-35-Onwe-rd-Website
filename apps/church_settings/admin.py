from django.contrib import admin

from .models import ChurchSettings, ServiceTime


@admin.register(ChurchSettings)
class ChurchSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identity", {"fields": ("church_name", "tagline", "logo", "favicon")}),
        ("Contact", {"fields": ("address", "phone_primary", "phone_secondary", "email")}),
        ("Social Links", {
            "fields": ("facebook_url", "instagram_url", "youtube_url",
                       "whatsapp_url", "x_url", "tiktok_url"),
        }),
        ("Map", {"fields": ("map_embed_url",)}),
        ("Footer", {"fields": ("footer_short_description",)}),
        ("Default SEO", {"fields": ("default_seo_title", "default_seo_description", "default_og_image")}),
    )

    def has_add_permission(self, request):
        # Enforce singleton at the admin UI level too: block "Add" once
        # a row already exists, so nobody accidentally creates a second one.
        return not ChurchSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ServiceTime)
class ServiceTimeAdmin(admin.ModelAdmin):
    list_display = ("name", "day", "start_time", "end_time", "location", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("day", "is_active")