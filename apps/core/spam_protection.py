from django.core.cache import cache

RATE_LIMIT_MAX_SUBMISSIONS = 5
RATE_LIMIT_WINDOW_SECONDS = 600  # 10 minutes


def is_rate_limited(request):
    """
    Simple per-IP throttle for public forms (contact form today; any
    future public form can reuse this). Not a security boundary against
    a determined attacker spoofing IPs — it's a proportionate deterrent
    against basic bot spam and accidental double-submission, which is
    the actual threat model for a church contact form per §21/§37.
    """
    ip = _get_client_ip(request)
    cache_key = f"rate_limit:contact:{ip}"
    count = cache.get(cache_key, 0)
    if count >= RATE_LIMIT_MAX_SUBMISSIONS:
        return True
    cache.set(cache_key, count + 1, timeout=RATE_LIMIT_WINDOW_SECONDS)
    return False


def _get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")