from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True

# Disable throttling in dev
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []

# Optional: SQLite for local dev without Docker
DATABASES = {
     "default": {
         "ENGINE": "django.db.backends.sqlite3",
         "NAME": BASE_DIR / "db.sqlite3",
     }
 }
