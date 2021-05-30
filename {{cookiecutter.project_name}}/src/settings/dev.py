from settings.common import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["*"]

SECRET_KEY = "Insecure:fXP7kny5q3oKDV6_yBjs-keX6oZfRqC9pz--LDJ42r8"

INSTALLED_APPS += [  # noqa: F405
    "django_extensions",
]
