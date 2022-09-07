from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password',
                  'mobile', 'gender']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'type']


class OnlyStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'type']


class UserStudentSerializer(serializers.ModelSerializer):
    student = OnlyStudentSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password',
                  'mobile', 'gender', 'student']


class OnlyRecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = ['id', 'status', 'type']


class UserRecruiterSerializer(serializers.ModelSerializer):
    recruiter = OnlyRecruiterSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password',
                  'mobile', 'gender', 'recruiter']


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Admin
        fields = ['id', 'user', 'status', 'type']


class RecruiterSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Recruiter
        fields = ['id', 'user', 'status', 'type']


class CompanySerializer(serializers.ModelSerializer):
    recruiter = RecruiterSerializer(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'recruiter', 'email', 'name',
                  'logo', 'description', 'type', 'status']


class OnlyCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    recruiter = RecruiterSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'recruiter', 'company', 'title',
                  'description', 'experience', 'skills', 'location', 'salary', 'start_date', 'end_date', 'status']


class OnlyJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'


class ApplySerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Apply
        fields = ['id', 'job', 'student', 'applydate', 'status']


class StringSerializer(serializers.Serializer):
    error = serializers.CharField(max_length=256)


# class ForgotPasswordUser(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)

#     fields = ['user',]
