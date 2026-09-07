from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter
def highlight(headline, accent):
    """
    Wraps `accent` (a substring of `headline`) in a gold <span> for the
    hero headline treatment (e.g. "A Place to Worship, Grow and Serve"
    with "Grow" in gold, matching the reference design).

    Uses format_html (not string concatenation) so both `headline` and
    `accent` are auto-escaped — safe even though this content comes from
    an admin-editable field, per §51.
    """
    if not accent or accent not in headline:
        return headline
    before, _, after = headline.partition(accent)
    return format_html('{}<span class="text-gold">{}</span>{}', before, accent, after)