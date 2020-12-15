from settings.common import *  # noqa: F401, F403

ALLOWED_HOSTS += [  # noqa: F405
    "{% raw %}{{base_url}}{% endraw %}",
]
