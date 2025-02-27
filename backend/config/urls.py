from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("backend.apps.homepage.urls")),
    path("courses/", include("backend.apps.courses.urls")),
    path("accounts/", include("backend.apps.accounts.urls")),
    path("students/", include("backend.apps.students.urls")),
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
