from datetime import datetime, timezone as dt_timezone


def get_media_items():
    """
    Read-only aggregation of every uploaded image/file across the
    project, for browsing purposes only — NOT a reusable asset picker.
    See Phase 12 Step 4 scoping note for why: building genuine
    upload-once-reuse-everywhere media would require re-architecting
    every ImageField/FileField in the project into a shared foreign
    key, which isn't justified by anything actually requested.

    Each entry: {url, label, source, uploaded_at}
    `source` is a human string identifying where it's used, so an
    admin can find their way back to the right edit screen.
    """
    items = []

    from apps.church_settings.models import ChurchSettings
    cs = ChurchSettings.load()
    for field_name, label in [("logo", "Church Logo"), ("favicon", "Favicon"), ("default_og_image", "Default OG Image")]:
        f = getattr(cs, field_name)
        if f:
            items.append({"url": f.url, "label": label, "source": "Church Settings", "uploaded_at": None})

    from apps.homepage.models import HomepageContent
    hc = HomepageContent.load()
    for field_name, label in [("hero_image", "Hero Image"), ("about_image", "About Image"), ("visit_cta_image", "Visit CTA Image")]:
        f = getattr(hc, field_name)
        if f:
            items.append({"url": f.url, "label": label, "source": "Homepage Content", "uploaded_at": None})

    from apps.ministries.models import Leader, Ministry
    for leader in Leader.objects.exclude(photo=""):
        items.append({"url": leader.photo.url, "label": leader.full_name, "source": "Leader Photo", "uploaded_at": None})
    for ministry in Ministry.objects.exclude(image=""):
        items.append({"url": ministry.image.url, "label": ministry.name, "source": "Ministry Image", "uploaded_at": None})

    from apps.sermons.models import Sermon
    for sermon in Sermon.objects.exclude(thumbnail=""):
        items.append({"url": sermon.thumbnail.url, "label": sermon.title, "source": "Teaching Thumbnail", "uploaded_at": sermon.created_at})

    from apps.events.models import Event
    for event in Event.objects.exclude(image=""):
        items.append({"url": event.image.url, "label": event.title, "source": "Event Image", "uploaded_at": event.created_at})

    from apps.news.models import Article
    for article in Article.objects.exclude(featured_image=""):
        items.append({"url": article.featured_image.url, "label": article.title, "source": "News Featured Image", "uploaded_at": article.created_at})

    from apps.gallery.models import GalleryImage
    for img in GalleryImage.objects.select_related("album"):
        items.append({"url": img.image.url, "label": img.display_alt, "source": f"Gallery: {img.album.title}", "uploaded_at": None})

    # Most recent first where we have a date; undated items (singletons,
    # no created_at field) sort last rather than crashing on None.

    items.sort(
        key=lambda i: i["uploaded_at"] or datetime.min.replace(tzinfo=dt_timezone.utc),
        reverse=True,
    )
    return items