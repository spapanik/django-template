from settings.common import *  # noqa: F401, F403

DEBUG = True

ROOT_URLCONF = "urls_dev"
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR.joinpath("emails")  # noqa: F405

SECRET_KEY = "Insecure:fXP7kny5q3oKDV6_yBjs-keX6oZfRqC9pz--LDJ42r8"

MIDDLEWARE += [  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INSTALLED_APPS += [  # noqa: F405
    "django_extensions",
    "debug_toolbar",
]
