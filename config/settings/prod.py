from .base import *

DEBUG = False

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

DATABASES = {
    "default": env.db("DATABASE_URL"),
}

# ── HTTPS enforcement ──────────────────────────────────────────
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 300  # 1 year, once confirmed working — see Phase 16 rollout note
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Render terminates TLS at its proxy and forwards plain HTTP internally,
# so Django needs to trust the proxy's header to know the original
# request was actually HTTPS — without this, SECURE_SSL_REDIRECT would
# incorrectly redirect every request in an infinite loop.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ── Cookies ────────────────────────────────────────────────────
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# ── Security headers ───────────────────────────────────────────
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# ── Session expiry ─────────────────────────────────────────────
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60 * 60 * 8  # 8 hours — a church admin's work session, not a permanent login

# ── Static/media (filled in fully in Phase 16 with django-storages) ──
STATIC_ROOT = BASE_DIR / "staticfiles"

# ── Logging — errors surfaced, nothing sensitive logged ────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.security": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    },
}