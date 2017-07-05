"""
Course API URI specification.
"""
from django.conf.urls import include, url, patterns

urlpatterns = patterns(
    '',

    url(r'^', include('organization_dashboard_api.v1.OrganizationAPI.urls')),
    url(r'^', include('organization_dashboard_api.v1.OrganizationApp.urls')),
)
