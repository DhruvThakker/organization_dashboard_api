"""
Organization API v1 URL specification
"""
from django.conf.urls import url, patterns
import views

urlpatterns = patterns(
    '',

    #url(r'^v1/summary/$', views.OrganizationList.as_view()),
    #url(r'^v1/summary/(?P<organization>[A-Za-z0-9+_.-]+)/$', views.OrganizationDetail.as_view()),
    #url(r'^count/$', views.OrganizationCountList.as_view()),
    #url(r'^count/(?P<organization>[A-Za-z0-9+_.-]+)/$', views.OrganizationCountDetail.as_view()),
    url(r'^grade/$', views.OrganizationGradeList.as_view()),
    url(r'^grade/(?P<organization>[A-Za-z0-9+_.-]+)/$', views.OrganizationGradeDetail.as_view()),
    url(r'^certificate/$', views.OrganizationCertificateList.as_view()),
    url(r'^certificate/(?P<organization>[A-Za-z0-9+_.-]+)/$', views.OrganizationCertificateDetail.as_view()),
)
