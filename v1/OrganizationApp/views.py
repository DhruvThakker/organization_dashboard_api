# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.
from rest_framework import viewsets,permissions,response,status,generics
from serializers import *
from OrgApiData import *
from django.http import Http404
from rest_framework.throttling import UserRateThrottle
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from oauth2_provider.ext.rest_framework.authentication import OAuth2Authentication

class UserThrottle(UserRateThrottle):

    rate = '40/minute'

    def allow_request(self, request, view):
        return super(UserThrottle, self).allow_request(request, view)

class OrganizationCoursesList(generics.ListAPIView):
    """
        **Use Case**

            * Get a paginated list of courses available on edX platform under 
              given organization OR all organizations.

                The list can be filtered based on faculty name.

                Each page in the list can contain up to 10 courses.


        **Example Requests**

            GET /api/courses/v2/organization/summary/

            GET /api/courses/v2/organization/summary/{organization name}

            GET /api/courses/v2/organization/details/

            GET /api/courses/v2/organization/details/{organization name}

            Note : If Organization name is not provided a list is obtained in 
                   which courses are grouped based on organization.
                   If Organization name is provided an instance is obtained which contains
                   list of courses present in that organization.


        **GET Response Values**

            On success with Response Code <200>

                * count: The number of Courses under given organization in the edX platform.

                * next: The URI to the next page of courses.

                * previous: The URI to the previous page of courses.

                * num_pages: The number of pages listing courses.

                * results:
                    A list is returned. Each collection in the list
                    contains these fields.
                    * organization_name             : Name of the Organization.
                    * organization_course_list      : List of Courses in that organization.

                        * course_id                 :Id of the course.
                        * course_display_name       :Display name of the course.
                        * course_start              :Course start date and time.
                        * course_end                :Course end date and time.
                        * course_registration_start :Course registration start date and time.
                        * course_registration_end   :Course registration end date and time.
                        * course_status             :Running status of course.
                        * course_team               :Course Team
                            * course_instructors    :List of course instructors.
                                * username          :Username of Course Instructor.
                                * email             :EmailId of Course Instructor.
                            * course_members        :List of course members.
                                * username          :Username of Course Member.
                                * email             :EmailId of Course Member.
                        * course_student_count      :Count of students enrolled in the course.
        
                        With  (/details/)
        
                        * course_grading_policy     :
                            * grader        :   List of different assignments type and their details like total number, weight, number of droppable.
                            * grade_cutoffs :   List of different grades of the course, with their individual range.

            **ERROR RESPONSES**

                * Response Code <404> NOT FOUND
                * Response Code <403> FORBIDDEN

        """

    http_method_names = ['get']
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = OrganizationCourseSummarySerializer
    throttle_classes = (UserThrottle,)
    def get_queryset(self):

        try:
            p = get_all_courses_with_org(True)
            if p == [] or None:
                raise Http404(u"Empty list and '%s.allow_empty' is False."
                              % self.__class__.__name__)
            return p
        except:
            raise Http404(u"Empty list and '%s.allow_empty' is False."
                          % self.__class__.__name__)
class OrganizationCourseInstance(generics.RetrieveAPIView):
    """
        **Use Case**

            * Get a paginated list of courses available on edX platform under 
              given organization OR all organizations.

                The list can be filtered based on faculty name.

                Each page in the list can contain up to 10 courses.


        **Example Requests**

            GET /api/courses/v2/organization/summary/

            GET /api/courses/v2/organization/summary/{organization name}

            GET /api/courses/v2/organization/details/

            GET /api/courses/v2/organization/details/{organization name}

            Note : If Organization name is not provided a list is obtained in 
                   which courses are grouped based on organization.
                   If Organization name is provided an instance is obtained which contains
                   list of courses present in that organization.


        **GET Response Values**

            On success with Response Code <200>

                * count: The number of Courses under given organization in the edX platform.

                * next: The URI to the next page of courses.

                * previous: The URI to the previous page of courses.

                * num_pages: The number of pages listing courses.

                * results:
                    A list is returned. Each collection in the list
                    contains these fields.
                    * organization_name             : Name of the Organization.
                    * organization_course_list      : List of Courses in that organization.

                        * course_id                 :Id of the course.
                        * course_display_name       :Display name of the course.
                        * course_start              :Course start date and time.
                        * course_end                :Course end date and time.
                        * course_registration_start :Course registration start date and time.
                        * course_registration_end   :Course registration end date and time.
                        * course_status             :Running status of course.
                        * course_team               :Course Team
                            * course_instructors    :List of course instructors.
                                * username          :Username of Course Instructor.
                                * email             :EmailId of Course Instructor.
                            * course_members        :List of course members.
                                * username          :Username of Course Member.
                                * email             :EmailId of Course Member.
                        * course_student_count      :Count of students enrolled in the course.
        
                        With  (/details/)
        
                        * course_grading_policy     :
                            * grader        :   List of different assignments type and their details like total number, weight, number of droppable.
                            * grade_cutoffs :   List of different grades of the course, with their individual range.

            **ERROR RESPONSES**

                * Response Code <404> NOT FOUND
                * Response Code <403> FORBIDDEN

        """

    http_method_names = ['get']
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = OrganizationCourseSummarySerializer
    throttle_classes = (UserThrottle,)
    def get_object(self):

        try:
            p = get_courses_with_organization(self.kwargs['org'], True)

            if p[0]['organization_course_list'] == [] or None:
                raise Http404(u"Empty list and '%s.allow_empty' is False."
                              % self.__class__.__name__)
            return p[0]
        except:
            raise Http404(u"Empty list and '%s.allow_empty' is False."
                          % self.__class__.__name__)
