import re

from django import template

register = template.Library()

YOUTUBE_PATTERNS = [
    r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([\w-]{11})",
]
VIMEO_PATTERN = r"vimeo\.com/(\d+)"


@register.filter
def embeddable_video_url(url):
    """
    Returns a safe iframe `src` ONLY for recognized YouTube/Vimeo URLs.
    Anything else returns None, so the template can fall back to a
    plain outbound link instead of embedding an unknown page in an
    iframe — same principle as the Church Settings map_embed_url
    domain restriction from Phase 4 (§53), applied to sermon video.
    """
    if not url:
        return None

    for pattern in YOUTUBE_PATTERNS:
        match = re.search(pattern, url)
        if match:
            return f"https://www.youtube.com/embed/{match.group(1)}"

    match = re.search(VIMEO_PATTERN, url)
    if match:
        return f"https://player.vimeo.com/video/{match.group(1)}"

    return None