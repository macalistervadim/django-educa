from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("", include("backend.apps.homepage.urls")),
    path("admin/", admin.site.urls),
    path("courses/", include("backend.apps.courses.urls")),
    path("accounts/", include("backend.apps.accounts.urls")),
    path("students/", include("backend.apps.students.urls")),
    path("api/", include("backend.api.v1.urls")),
    path("chat/", include("backend.apps.chat.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]


if settings.DEBUG:
    urlpatterns += static(  # type: ignore
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
