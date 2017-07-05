from rest_framework import serializers

class CourseSummarySerializer(serializers.Serializer):
    course_id = serializers.CharField()
    course_display_name = serializers.CharField(allow_null=True)
    course_start = serializers.DateTimeField(allow_null=True)
    course_end = serializers.DateTimeField(allow_null=True)
    course_registration_start = serializers.DateTimeField(allow_null=True)
    course_registration_end = serializers.DateTimeField(allow_null=True)
    course_status = serializers.CharField(allow_null=True)
    course_team = serializers.DictField(allow_null=True)
    course_student_count = serializers.CharField(allow_null=True) #<- Last Edit

class CourseDetailsSerializer(serializers.Serializer):
    course_id = serializers.CharField()
    course_display_name = serializers.CharField(allow_null=True)
    course_start = serializers.DateTimeField(allow_null=True)
    course_end = serializers.DateTimeField(allow_null=True)
    course_registration_start = serializers.DateTimeField(allow_null=True)
    course_registration_end = serializers.DateTimeField(allow_null=True)
    course_status = serializers.CharField(allow_null=True)
    course_team = serializers.DictField(allow_null=True)
    course_student_count = serializers.CharField(allow_null=True) #<- Last Edit
    course_grading_policy = serializers.DictField(allow_null=True)

class OrganizationCourseSummarySerializer(serializers.Serializer):

    organization_name = serializers.CharField()
    organization_course_list = CourseSummarySerializer(many=True)

class OrganizationCourseDetailsSerializer(serializers.Serializer):

    organization_name = serializers.CharField()
    organization_course_list = CourseDetailsSerializer(many=True)
