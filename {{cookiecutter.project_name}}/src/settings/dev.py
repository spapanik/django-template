from settings.common import *  # noqa: F401, F403

DEBUG = True

SECRET_KEY = "An insecure secret key for development"

INSTALLED_APPS += [  # noqa: F405
    "django_extensions",
]
