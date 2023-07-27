from django.conf import settings
from django.contrib import admin
from django.urls import include, path


app_name = "core"
urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("", include("blog.urls")),
    path("admin/", admin.site.urls),
]

# fmt: off
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls))
    ]
# fmt: on
