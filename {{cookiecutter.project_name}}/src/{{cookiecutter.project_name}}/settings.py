import contextlib
import pathlib
from functools import partial

import django_stubs_ext
from dj_settings.utils import setting

BASE_DIR = pathlib.Path(__file__).parents[2]
project_setting = partial(setting, base_dir=BASE_DIR, filename="cc_bz_project_name.yml")
django_stubs_ext.monkeypatch()

# region Security
validation = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{validation}.UserAttributeSimilarityValidator"},
    {"NAME": f"{validation}.MinimumLengthValidator"},
    {"NAME": f"{validation}.CommonPasswordValidator"},
    {"NAME": f"{validation}.NumericPasswordValidator"},
]

SECRET_KEY = project_setting(
    "SECRET_KEY",
    sections=["project", "security"],
    default="Insecure:fXP7kny5q3oKDV6_yBjs-keX6oZfRqC9pz--LDJ42r8",
)
BASE_SCHEME = project_setting(
    "BASE_SCHEME", sections=["project", "security"], default="https"
)
if BASE_SCHEME == "https":
    SECURE_PROXY_SSL_HEADER = "HTTP_X_FORWARDED_PROTO", "https"
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
# endregion

# region Application definition
DEBUG = project_setting("DEBUG", sections=["project", "app"], rtype=bool, default=True)
ALLOWED_HOSTS = project_setting(
    "ALLOWED_HOSTS",
    sections=["project", "servers"],
    rtype=list,
    default=["localhost", "127.0.0.1"],
)
BASE_DOMAIN = ALLOWED_HOSTS[0]
BASE_PORT = project_setting(
    "BASE_PORT", sections=["project", "servers"], rtype=int, default=8000
)

AUTH_USER_MODEL = "accounts.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ROOT_URLCONF = "cc_bz_project_name.urls"

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "cc_bz_project_name.branding",
    "grappelli.dashboard",
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cc_bz_project_name.lib",
    "cc_bz_project_name.accounts",
    "cc_bz_project_name.home",
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
EMAIL_FILE_PATH = BASE_DIR.joinpath("local", "emails")

MIGRATION_HASHES_PATH = BASE_DIR.joinpath("migrations.lock")

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

OPTIMUS_PRIME = project_setting(
    "OPTIMUS_PRIME", sections=["project", "app", "optimus"], rtype=int, default=1
)
OPTIMUS_INVERSE = project_setting(
    "OPTIMUS_INVERSE", sections=["project", "app", "optimus"], rtype=int, default=1
)
OPTIMUS_RANDOM = project_setting(
    "OPTIMUS_RANDOM", sections=["project", "app", "optimus"], rtype=int, default=0
)
# endregion

# region Databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "cc_bz_project_name",
    },
}
# endregion

# region Static files
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    },
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

# region 3rd party
GRAPPELLI_INDEX_DASHBOARD = "cc_bz_project_name.home.dashboard.AdminDashboard"
GRAPPELLI_ADMIN_TITLE = "cc_bz_project_name"
# endregion

with contextlib.suppress(ImportError):
    from cc_bz_project_name.local.settings import *  # noqa: F403
