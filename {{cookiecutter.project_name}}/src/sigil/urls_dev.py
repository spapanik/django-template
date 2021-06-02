import debug_toolbar

from django.urls import include, path

from sigil.urls import urlpatterns

urlpatterns += [
    path("__debug__/", include(debug_toolbar.urls)),
]
