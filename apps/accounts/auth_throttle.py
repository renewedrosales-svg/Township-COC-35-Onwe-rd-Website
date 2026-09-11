from django.core.cache import cache

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_SECONDS = 15 * 60  # 15 minutes


def _cache_key(username, ip):
    return f"login_throttle:{username}:{ip}"


def is_locked_out(username, ip):
    return cache.get(_cache_key(username, ip), 0) >= MAX_FAILED_ATTEMPTS


def record_failed_attempt(username, ip):
    key = _cache_key(username, ip)
    count = cache.get(key, 0) + 1
    cache.set(key, count, LOCKOUT_SECONDS)
    return count


def clear_attempts(username, ip):
    cache.delete(_cache_key(username, ip))


def get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
