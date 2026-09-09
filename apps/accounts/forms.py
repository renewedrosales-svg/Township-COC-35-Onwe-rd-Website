from django.contrib.auth.forms import AuthenticationForm

from apps.core.forms import TailwindStyledFormMixin


class StyledLoginForm(TailwindStyledFormMixin, AuthenticationForm):
    """
    Django's AuthenticationForm styled with our standard input classes
    (TailwindStyledFormMixin, same as every dashboard content form
    since Phase 12) — the login page was the one form in the project
    still using bare, unstyled widgets, left over from Phase 3 when
    we deliberately deferred styling it. Fixing that properly now
    rather than styling it as a one-off.
    """
    pass