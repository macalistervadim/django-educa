from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("src.apps.homepage.urls")),
    path("courses/", include("src.apps.courses.urls")),
    path("accounts/", include("src.apps.accounts.urls")),
    path("grappelli/", include("grappelli.urls")),
    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(  # type: ignore
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

    import debug_toolbar

    urlpatterns += [
        path(
            "__debug__/",
            include(debug_toolbar.urls),
        ),
    ]
