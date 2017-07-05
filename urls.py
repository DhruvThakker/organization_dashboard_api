"""
Course API URI specification.
Patterns here should simply point to version-specific patterns.
"""
from django.conf.urls import include, url, patterns

urlpatterns = patterns(
    '',

    url(r'^v1/', include('organization_dashboard_api.v1.urls')),
)
