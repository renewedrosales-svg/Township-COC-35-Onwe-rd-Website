from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from apps.core.forms import TailwindStyledFormMixin

from .auth_throttle import (
    clear_attempts,
    get_client_ip,
    is_locked_out,
    record_failed_attempt,
)


class StyledLoginForm(TailwindStyledFormMixin, AuthenticationForm):
    """
    Styled AuthenticationForm (Phase 12) with brute-force protection
    added (Phase 15, §37/§38). Locked by username+IP together, not
    username alone, so an attacker can't lock out a legitimate user's
    account just by repeatedly failing their login from elsewhere —
    see Phase 15 Step 1 for the full reasoning.
    """

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(request=request, *args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username")
        ip = get_client_ip(self.request) if self.request else "unknown"

        if username and is_locked_out(username, ip):
            raise ValidationError(
                "Too many failed login attempts. Please wait 15 minutes and try again.",
                code="locked_out",
            )

        try:
            cleaned_data = super().clean()
        except ValidationError:
            if username:
                record_failed_attempt(username, ip)
            raise

        if username:
            clear_attempts(username, ip)
        return cleaned_data