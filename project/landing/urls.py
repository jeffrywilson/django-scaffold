from django.conf import settings
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from landing.views import LandingView, VersionView
from . import views


urlpatterns = [
    #path("", TemplateView.as_view(template_name="landing/index.html"), name="home"),
    path("", LandingView.as_view(), name="home"),
    path(
        "privacy_policy/",
        TemplateView.as_view(template_name="landing/privacy_policy.html"),
        name="privacy.policy",
    ),
    path(
        "version/",
        VersionView.as_view(template_name="landing/version.html"),
        name="version",
    ),
    path(
        "terms_and_conditions/",
        TemplateView.as_view(template_name="landing/terms_and_conditions.html"),
        name="terms.and.conditions",
    ),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            "robots.txt/",
            TemplateView.as_view(
                template_name="landing/no_robots.txt", content_type="text/plain"
            ),
        )
    ]
else:
    urlpatterns += [
        path(
            "robots.txt/",
            TemplateView.as_view(
                template_name="landing/robots.txt", content_type="text/plain"
            ),
        )
    ]
