import contextlib
import pathlib
from datetime import timedelta
from functools import partial

import django_stubs_ext
from dj_settings import get_setting

BASE_DIR = pathlib.Path(__file__).parents[2]
project_setting = partial(
    get_setting, project_dir=BASE_DIR, filename="{{cookiecutter.project_name}}.yml"
)
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

signup_token_expiry = project_setting(
    "SIGNUP_TOKEN_EXPIRY",
    sections=["project", "tokens"],
    rtype=dict,
    default={"days": 31},
)
SIGNUP_TOKEN_EXPIRY = timedelta(**signup_token_expiry)
access_token_expiry = project_setting(
    "ACCESS_TOKEN_EXPIRY",
    sections=["project", "tokens"],
    rtype=dict,
    default={"days": 365},
)
ACCESS_TOKEN_EXPIRY = timedelta(**access_token_expiry)
refresh_token_expiry = project_setting(
    "REFRESH_TOKEN_EXPIRY",
    sections=["project", "tokens"],
    rtype=dict,
    default={"days": 3650},
)
REFRESH_TOKEN_EXPIRY = timedelta(**refresh_token_expiry)
# endregion

# region Application definition
DEBUG = project_setting("DEBUG", sections=["project", "app"], rtype=bool, default=True)
BARE_DOMAIN = project_setting(
    "BARE_DOMAIN", sections=["project", "servers"], default="localhost"
)
BASE_API_DOMAIN = project_setting(
    "BASE_API_DOMAIN", sections=["project", "servers"], default="localhost"
)
BASE_API_PORT = project_setting(
    "BASE_API_PORT", sections=["project", "servers"], rtype=int, default=8000
)
EXTRA_API_DOMAINS = project_setting(
    "EXTRA_API_DOMAINS",
    sections=["project", "servers"],
    rtype=list,
    default=["127.0.0.1"],
)
BASE_APP_DOMAIN = project_setting(
    "BASE_APP_DOMAIN", sections=["project", "servers"], default="localhost"
)
BASE_APP_PORT = project_setting(
    "BASE_APP_PORT", sections=["project", "servers"], rtype=int, default=3000
)
EXTRA_APP_DOMAINS = project_setting(
    "EXTRA_APP_DOMAINS",
    sections=["project", "servers"],
    rtype=list,
    default=["127.0.0.1"],
)
ALLOWED_HOSTS = [
    BASE_API_DOMAIN,
    *EXTRA_API_DOMAINS,
    BASE_APP_DOMAIN,
    *EXTRA_APP_DOMAINS,
]

AUTH_USER_MODEL = "users.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ROOT_URLCONF = "{{cookiecutter.project_name}}.urls"

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "{{cookiecutter.project_name}}.lib",
    "{{cookiecutter.project_name}}.users",
    "{{cookiecutter.project_name}}.home",
]

if DEBUG:
    INSTALLED_APPS += [
        "django_extensions",
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR.joinpath("local", "emails")

MIGRATION_HASHES_PATH = BASE_DIR.joinpath("migrations.lock")

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
        "NAME": "{{cookiecutter.project_name}}",
    },
}
# endregion

# region i18n/l10n
TIME_ZONE = "UTC"
# endregion

with contextlib.suppress(ImportError):
    from {{cookiecutter.project_name}}.local.settings import *  # noqa: F403
