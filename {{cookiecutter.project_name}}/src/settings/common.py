import pathlib

BASE_DIR = pathlib.Path(__file__).parents[2]

# region Security
validation = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{validation}.UserAttributeSimilarityValidator"},
    {"NAME": f"{validation}.MinimumLengthValidator"},
    {"NAME": f"{validation}.CommonPasswordValidator"},
    {"NAME": f"{validation}.NumericPasswordValidator"},
]

SECURE_PROXY_SSL_HEADER = "HTTP_X_FORWARDED_PROTO", "https"
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 604800
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# endregion

# region Application definition
ROOT_URLCONF = "urls"
WSGI_APPLICATION = "wsgi.application"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "lib",
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

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
# endregion

# region Databases
DATABASES = {
    "default": {"ENGINE": "django.db.backends.postgresql", "NAME": "{{cookiecutter.project_name}}"}
}
# endregion

# region Static filed
STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR.joinpath(".static")
# endregion

# region i18n/l10n
LANGUAGE_CODE = "en"

LANGUAGES = [("en", "English")]

LOCALE_PATHS = [BASE_DIR.joinpath("locale")]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True
# endregion
