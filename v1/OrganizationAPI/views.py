from rest_framework import generics
from api import *
from serializers import OrganizationSerializer, OrganizationStudentSerializer, OrganizationGradeSerializer, OrganizationCertificateSerializer
from rest_framework.permissions import IsAdminUser
from django.http import Http404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from oauth2_provider.ext.rest_framework.authentication import OAuth2Authentication

# Create your views here.


class OrganizationList(generics.ListAPIView):
    """
        **Use Case**

            *Get a paginated list of organizations with all its courses in the edX Platform.

                Each page in the list can contain up to 10 courses.

        **Example Requests**

              GET /api/organizations/v1/summary/

        **Response Values**

            On success with Response Code <200>

            * count: The number of courses in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:  A list of courses returned. Each collection in the list
              contains these fields.

                * organization: The name of the organization.

                * courses: 

                    * id: The unique identifier for the course.

                    * display_name: The display name of the course.

                    * start: The course start date.

                    * end: The course end date. If course end date is not specified, the
                        value is null.

                    * enrollment_start: The course enrollment start date.

                    * enrollment_end: The course enrollment end date. If course enrollment end date is not 
                        specified, the value is null.


         **ERROR RESPONSES**

                * Response Code <403> FORBIDDEN

        """
    queryset = get_all_organization()
    serializer_class = OrganizationSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)


class OrganizationDetail(generics.RetrieveAPIView):
    """
        **Use Case**

            Get all the courses for a specific organization.

        **Example Requests**

              GET /api/organizations/v1/summary/{organization_name}

        **Response Values**

            On success with Response Code <200>

            * organization: The name of the organization.

            * courses: 

                * id: The unique identifier for the course.

                * display_name: The display name of the course.

                * start: The course start date.

                * end: The course end date. If course end date is not specified, the
                    value is null.

                * enrollment_start: The course enrollment start date.

                * enrollment_end: The course enrollment end date. If course enrollment end date is not 
                    specified, the value is null.

         **ERROR RESPONSES**

                * Response Code <404> ORGANIZATION NOT FOUND
                * Response Code <403> FORBIDDEN

        """
    serializer_class = OrganizationSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)

    def get_object(self):
        try:
            organization = self.kwargs['organization']
            list = get_all_courses(organization)
            list['organization']
            return list
        except:
            raise Http404


class OrganizationCountList(generics.ListAPIView):
    """
        **Use Case**

            *Get a paginated list of organizations with all its courses and count of students in the edX Platform.

                Each page in the list can contain up to 10 courses.

        **Example Requests**

              GET /api/organizations/v1/count/

        **Response Values**

            On success with Response Code <200>

            * count: The number of courses in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:  A list of courses returned. Each collection in the list
              contains these fields.

                * organization: The name of the organization.

                * courses: 

                    * id: The unique identifier for the course.

                    * display_name: The display name of the course.

                    * start: The course start date.

                    * end: The course end date. If course end date is not specified, the
                        value is null.

                    * enrollment_start: The course enrollment start date.

                    * enrollment_end: The course enrollment end date. If course enrollment end date is not 
                        specified, the value is null.
                        
                    * students: Count of students in the course

         **ERROR RESPONSES**

                * Response Code <403> FORBIDDEN

        """
    queryset = get_all_organization_count_students()
    serializer_class = OrganizationStudentSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)


class OrganizationCountDetail(generics.RetrieveAPIView):
    """
        **Use Case**

            Get all the courses and count of students for a specific organization.

        **Example Requests**

              GET /api/organizations/v1/count/{organization_name}

        **Response Values**

            On success with Response Code <200>

            * organization: The name of the organization.

            * courses: 

                * id: The unique identifier for the course.

                * display_name: The display name of the course.

                * start: The course start date.

                * end: The course end date. If course end date is not specified, the
                    value is null.

                * enrollment_start: The course enrollment start date.

                * enrollment_end: The course enrollment end date. If course enrollment end date is not 
                    specified, the value is null.
                        
                * students: Count of students in the course

         **ERROR RESPONSES**

                * Response Code <404> ORGANIZATION NOT FOUND
                * Response Code <403> FORBIDDEN

        """
    serializer_class = OrganizationStudentSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)

    def get_object(self):
        try:
            organization = self.kwargs['organization']
            list = get_all_courses_count_students(organization)
            list['organization']
            return list
        except:
            raise Http404


class OrganizationGradeList(generics.ListAPIView):
    """
        **Use Case**

            *Get a paginated list of organization with all its courses and students in the edX Platform.

                Each page in the list can contain up to 10 courses.

        **Example Requests**

              GET /api/organizations/v1/grade/

        **Response Values**

            On success with Response Code <200>

            * count: The number of courses in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:  A list of courses returned. Each collection in the list
              contains these fields.

                * organization: The name of the organization.

                * courses: 

                    * course_name: Name of the course
              
                    * course_organization: The organization specified for the course.
                
                    * course_run: The run of the course
                        
                    * students:
                    
                        * id: The unique identifier for the student.

                        * username: Username of the student
                    
                        * email: Email of the student
                    
                        * grade: Overall grade of the student in the course
                        
                        * total_score: Total score of the student in the course
                        
                        * is_active: Shows whether the student is active or not
                            1: if student is active
                            0: if student is not active
                            
                        * last_login: The date and time at which the student was last active

         **ERROR RESPONSES**

                * Response Code <403> FORBIDDEN

        """
    queryset = get_all_organization_courses_grades()
    serializer_class = OrganizationGradeSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)


class OrganizationGradeDetail(generics.RetrieveAPIView):
    """
        **Use Case**

            Get all the courses and students for a specific organization.

        **Example Requests**

              GET /api/organizations/v1/grade/{organization_name}

        **Response Values**

            On success with Response Code <200>

            * organization: The name of the organization.

            * courses: 

                * course_name: Name of the course
              
                * course_organization: The organization specified for the course.
                
                * course_run: The run of the course
                        
                * students:
                    
                    * id: The unique identifier for the student.

                    * username: Username of the student
                    
                    * email: Email of the student
                    
                    * grade: Overall grade of the student in the course
                    
                    * total_score: Total score of the student in the course
                        
                    * is_active: Shows whether the student is active or not
                        1: if student is active
                        0: if student is not active
                            
                    * last_login: The date and time at which the student was last active

         **ERROR RESPONSES**

                * Response Code <404> ORGANIZATION NOT FOUND
                * Response Code <403> FORBIDDEN

        """
    serializer_class = OrganizationGradeSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)

    def get_object(self):
        try:
            organization = self.kwargs['organization']
            list = get_all_courses_grades(organization)
            list['organization']
            return list
        except:
            raise Http404


class OrganizationCertificateList(generics.ListAPIView):
    """
        **Use Case**

            *Get a paginated list of organization with all its courses and count of certificates in the edX Platform.

                Each page in the list can contain up to 10 courses.

        **Example Requests**

              GET /api/organizations/v1/certificate/

        **Response Values**

            On success with Response Code <200>

            * count: The number of courses in the edX platform.

            * next: The URI to the next page of courses.

            * previous: The URI to the previous page of courses.

            * num_pages: The number of pages listing courses.

            * results:  A list of courses returned. Each collection in the list
              contains these fields.
              
                * organization: The name of the organization.

                * courses: 
              
                    * course_id: The unique identifier for the course.

                    * course_name: Name of the course

                    * course_organization: The organization specified for the course.

                    * course_run: The run of the course.
                
                    * certificate_count: Count of certificates of the course

         **ERROR RESPONSES**

                * Response Code <403> FORBIDDEN

        """
    queryset = get_all_organization_certificate_count()
    serializer_class = OrganizationCertificateSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)


class OrganizationCertificateDetail(generics.RetrieveAPIView):
    """
        **Use Case**

            Get all the courses and count of certificates for a specific organization.

        **Example Requests**

              GET /api/organizations/v1/certificate/{organization_name}

        **Response Values**

            On success with Response Code <200>

            * organization: The name of the organization.

            * courses: 
              
                * course_id: The unique identifier for the course.

                * course_name: Name of the course

                * course_organization: The organization specified for the course.

                * course_run: The run of the course.
                
                * certificate_count: Count of certificates of the course

         **ERROR RESPONSES**

                * Response Code <404> ORGANIZATION NOT FOUND
                * Response Code <403> FORBIDDEN

        """
    serializer_class = OrganizationCertificateSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, OAuth2Authentication)

    def get_object(self):
        try:
            organization = self.kwargs['organization']
            list = get_organization_certificate_count(organization )
            list['organization']
            return list
        except:
            raise Http404