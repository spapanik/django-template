import contextlib
import pathlib
from functools import partial

from dj_settings.utils import setting
from pathurl import URL

BASE_DIR = pathlib.Path(__file__).parents[2]
bmk_setting = partial(setting, base_dir=BASE_DIR, filename="bmk.yml")

# region Security
validation = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{validation}.UserAttributeSimilarityValidator"},
    {"NAME": f"{validation}.MinimumLengthValidator"},
    {"NAME": f"{validation}.CommonPasswordValidator"},
    {"NAME": f"{validation}.NumericPasswordValidator"},
]

SECRET_KEY = bmk_setting(
    "SECRET_KEY",
    sections=["bmk", "security"],
    default="Insecure:fXP7kny5q3oKDV6_yBjs-keX6oZfRqC9pz--LDJ42r8",
)

BASE_SCHEME = "https"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", BASE_SCHEME)
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# endregion

# region Application definition
DEBUG = bmk_setting("DEBUG", sections=["bmk", "app"], rtype=bool, default=True)
BASE_DOMAIN = bmk_setting("BASE_DOMAIN", sections=["bmk", "servers"])
ALLOWED_HOSTS = [BASE_DOMAIN]
BASE_URL = URL(f"{BASE_SCHEME}://{BASE_DOMAIN}")

AUTH_USER_MODEL = "registration.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ROOT_URLCONF = "bmk.urls"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "{{cookiecutter.project_name}}.home",
    "{{cookiecutter.project_name}}.registration",
]

if DEBUG:
    INSTALLED_APPS += [
        "django_extensions",
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR.joinpath("emails")

MIGRATION_HASHES_PATH = BASE_DIR.joinpath("migrations.lock")

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
# endregion

# region Databases
DATABASES = {
    "default": {"ENGINE": "django.db.backends.postgresql", "NAME": "{{cookiecutter.project_name}}"}
}
# endregion

# region Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR.joinpath(".static")
# endregion

# region i18n/l10n
LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English")]

LOCALE_PATHS = [BASE_DIR.joinpath("locale")]

TIME_ZONE = "UTC"
USE_TZ = True
# endregion

with contextlib.suppress(ImportError):
    from bmk.local.settings import *  # noqa: F401, F403
