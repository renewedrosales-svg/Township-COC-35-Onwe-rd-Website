from django.contrib import admin

from .models import CreedItem, HomepageContent


@admin.register(HomepageContent)
class HomepageContentAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Hero Section", {
            "fields": ("hero_eyebrow", "hero_headline", "hero_headline_accent",
                       "hero_description", "hero_image",
                       "hero_cta_primary_text", "hero_cta_primary_url",
                       "hero_cta_secondary_text", "hero_cta_secondary_url"),
        }),
        ("About Preview", {
            "fields": ("about_eyebrow", "about_heading", "about_description",
                       "about_image", "about_cta_text", "about_cta_url"),
        }),
        ("Visit Us CTA Banner", {
            "fields": ("visit_cta_heading", "visit_cta_description", "visit_cta_image",
                       "visit_cta_button_text", "visit_cta_button_url"),
        }),
        ("Section Visibility", {
            "fields": ("show_creed_section", "show_about_section",
                       "show_service_times_section", "show_events_section",
                       "show_sermons_section", "show_ministries_section",
                       "show_news_section", "show_gallery_section",
                       "show_school_section", "show_visit_cta_section"),
            "description": "Sections for apps not built yet are OFF by default. "
                            "They'll be enabled as each phase completes.",
        }),
    )

    def has_add_permission(self, request):
        return not HomepageContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CreedItem)
class CreedItemAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")