from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


admin.site.site_header = "Blog Admin Panel"
admin.site.site_title = "Site Administration"
admin.site.index_title = "Blog Admin"


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
        path("__debug__/", include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# fmt: on
