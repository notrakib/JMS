from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email',
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
        fields = ['id', 'name', 'email',
                  'mobile', 'gender', 'student']


class OnlyRecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = ['id', 'status', 'type']


class UserRecruiterSerializer(serializers.ModelSerializer):
    recruiter = OnlyRecruiterSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email',
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
                  'description', 'type', 'status']


class OnlyCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    recruiter = RecruiterSerializer(read_only=True)
    company = OnlyCompanySerializer(read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'recruiter', 'company', 'title',
                  'description', 'experience', 'skills', 'location', 'salary', 'start_date', 'end_date', 'status']


class OnlyJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'


class CompanyJobSerializer(serializers.ModelSerializer):
    company = OnlyCompanySerializer(read_only=True)

    class Meta:
        model = Job
        fields = ['id',  'company', 'title',
                  'description', 'experience', 'skills', 'location', 'salary', 'start_date', 'end_date', 'status']


class ApplySerializer(serializers.ModelSerializer):
    job = OnlyJobSerializer(read_only=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Apply
        fields = ['id', 'job', 'student', 'applydate', 'status']


class ApplyJobSerializer(serializers.ModelSerializer):
    job = OnlyJobSerializer(read_only=True)

    class Meta:
        model = Apply
        fields = ['id', 'job', 'applydate', 'status']


class ApplyStudentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Apply
        fields = ['id', 'student', 'applydate', 'status']
