from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("", include("apps.courses.urls")),
    path("accounts/", include("apps.users.urls")),
    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += (
        static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        )
        + debug_toolbar_urls()
    )
