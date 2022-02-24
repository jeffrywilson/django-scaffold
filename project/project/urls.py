from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from user_registration.urls import urlpatterns as registration_patterns

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('411/', admin.site.urls),
    path("hijack/", include('hijack.urls', namespace='hijack')),
    path("", include(registration_patterns)),
    path("", include("landing.urls")),
    # API Urls set
    path("api/", include("api.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns