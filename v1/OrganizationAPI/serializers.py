""" Django REST Framework Serializers """
from rest_framework import serializers


class CourseSerializer(serializers.Serializer):
    """ Serializer for Courses """
    id = serializers.CharField()
    display_name = serializers.CharField()
    start = serializers.DateField(allow_null=True)
    end = serializers.DateField(allow_null=True)
    enrollment_start = serializers.DateField(allow_null=True)
    enrollment_end = serializers.DateField(allow_null=True)


class OrganizationSerializer(serializers.Serializer):
    """ Serializer for Organization with all its courses """
    organization = serializers.CharField()
    courses = CourseSerializer(many=True, allow_null=True)


class CourseStudentSerializer(serializers.Serializer):
    """ Serializer for Courses with count of students """
    id = serializers.CharField()
    display_name = serializers.CharField()
    start = serializers.DateField(allow_null=True)
    end = serializers.DateField(allow_null=True)
    enrollment_start = serializers.DateField(allow_null=True)
    enrollment_end = serializers.DateField(allow_null=True)
    students = serializers.IntegerField()


class OrganizationStudentSerializer(serializers.Serializer):
    """ Serializer for Organization with all its courses and count of students """
    organization = serializers.CharField()
    courses = CourseStudentSerializer(many=True, allow_null=True)


class StudentSerializer(serializers.Serializer):
    """ Serializer for Student """
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    total_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    grade = serializers.CharField(allow_null=True)
    is_active = serializers.IntegerField()
    last_login = serializers.DateTimeField()


class CourseGradeSerializer(serializers.Serializer):
    """ Serializer for Course with all its students and their grades """
    course_name = serializers.CharField()
    course_organization = serializers.CharField()
    course_run = serializers.CharField()
    students = StudentSerializer(many=True, allow_null=True)


class OrganizationGradeSerializer(serializers.Serializer):
    """ Serializer for Organization with all its courses and students """
    organization = serializers.CharField()
    courses = CourseGradeSerializer(many=True, allow_null=True)


class CourseCertificateSerializer(serializers.Serializer):
    """ Serializer for Courses with count of certificates """
    course_id = serializers.CharField()
    course_name = serializers.CharField()
    course_run = serializers.CharField()
    course_organization = serializers.CharField()
    certificate_count = serializers.IntegerField()


class OrganizationCertificateSerializer(serializers.Serializer):
    """ Serializer for Organization with all its courses and count of certificates """
    organization = serializers.CharField()
    courses = CourseCertificateSerializer(many=True, allow_null=True)