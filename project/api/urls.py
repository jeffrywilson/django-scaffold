from django.conf.urls import url
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from user_registration.urls import api_patterns as registration_api_patterns

# Documentation Schema settings for generating API Docs
schema_view = get_schema_view(
    openapi.Info(
        title="Django-Scaffold API",
        default_version="v1",
        description="Base API for the Django-Scaffold Project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="info@ideamaker.agency"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("v1/", include(registration_api_patterns)),
    path("v1/docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]




