from django.conf.urls import url
import views

from serializers import *

urlpatterns = [


    url(r'^summary/$',views.OrganizationCoursesList.as_view()),
    url(r'^summary/(?P<org>[A-Za-z0-9._-]+)/$',views.OrganizationCourseInstance.as_view()),
    url(r'^details/$',views.OrganizationCoursesList.as_view(serializer_class=OrganizationCourseDetailsSerializer)),
    url(r'^details/(?P<org>[A-Za-z0-9._-]+)/$',views.OrganizationCourseInstance.as_view(serializer_class=OrganizationCourseDetailsSerializer)),


]
