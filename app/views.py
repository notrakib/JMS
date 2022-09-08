from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from datetime import date
import random
from django.utils.decorators import decorator_from_middleware
from app.middleware.middleware_session import session_middleware
import bcrypt

from functools import wraps
import json
from django.http import HttpResponseForbidden
import jwt


def custom_view_decorator(view_function):
    @wraps(view_function)
    def wrap(request, *args, **kwargs):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split()
            user = jwt.decode(token[1], key='ami_rakib',
                              algorithms=['HS256', ])

            request.curr_user = user
            return view_function(request, *args, **kwargs)

        except Exception as e:
            return view_function(request, *args, **kwargs)

    return wrap


@api_view(['POST'])
def AdminSignUp(request):

    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    # image = request.FILES.get('image')
    mobile = request.data.get('mobile')
    gender = request.data.get('gender')

    try:
        hashed = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

        user = User.objects.create(
            name=name, email=email, password=hashed.decode('utf-8'),  mobile=mobile, gender=gender)

        admin = Admin.objects.create(
            user=user)

        serializer = AdminSerializer(admin)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def StudentSignUp(request):

    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    # image = request.FILES.get('image')
    mobile = request.data.get('mobile')
    gender = request.data.get('gender')

    # resume = request.FILES.get('resume')
    try:
        hashed = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

        user = User.objects.create(
            name=name, email=email, password=hashed.decode('utf-8'),  mobile=mobile, gender=gender)

        student = Student.objects.create(
            user=user)

        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def RecruiterSignUp(request):

    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    # image = request.FILES.get('image')
    mobile = request.data.get('mobile')
    gender = request.data.get('gender')

    try:
        hashed = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

        user = User.objects.create(
            name=name, email=email, password=hashed.decode('utf-8'),  mobile=mobile, gender=gender)

        recruiter = Recruiter.objects.create(
            user=user)

        serializer = RecruiterSerializer(recruiter)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@custom_view_decorator
@api_view(['POST'])
def CreateCompany(request):

    if request.curr_user.get('type') == 'recruiter':

        if Recruiter.objects.get(pk=request.curr_user.get('id')).status == 'accepted':

            email = request.data.get('email')
            name = request.data.get('name')
            # logo = request.FILES.get('logo')
            description = request.data.get('description')
            type = request.data.get('type')

            try:
                company = Company.objects.create(recruiter=Recruiter.objects.get(pk=request.curr_user.get('id')),
                                                 email=email, name=name,  description=description, type=type)

                serializer = CompanySerializer(company)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Recruiter needs to be accepted'}, status=status.HTTP_403_FORBIDDEN)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def AdminSignIn(request):

    email = request.data.get('email')
    password = request.data.get('password')

    try:
        admin = Admin.objects.filter(user__email=email)

        if admin:

            if bcrypt.checkpw(bytes(password, 'utf-8'), admin[0].user.password.encode('utf-8')):

                payload_data = {
                    "id": admin[0].id,
                    "email": admin[0].user.email,
                    "type": admin[0].type,
                    "status": admin[0].status
                }
                token = jwt.encode(
                    payload=payload_data,
                    key='ami_rakib'
                )

                return Response({'token': token, 'payload_data': payload_data}, status=status.HTTP_200_OK)
            else:
                raise Exception('Invalid Password')

        else:
            raise Exception('Invalid Email')

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def StudentSignIn(request):

    email = request.data.get('email')
    password = request.data.get('password')

    try:
        student = Student.objects.filter(user__email=email)

        if student.exists():

            if bcrypt.checkpw(bytes(password, 'utf-8'), student[0].user.password.encode('utf-8')):

                payload_data = {
                    "id": student[0].id,
                    "email": student[0].user.email,
                    "type": student[0].type
                }
                token = jwt.encode(
                    payload=payload_data,
                    key='ami_rakib'
                )

                return Response({'token': token, 'payload_data': payload_data}, status=status.HTTP_200_OK)
            else:
                raise Exception('Invalid Password')

        else:
            raise Exception('Invalid Email')

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def RecruiterSignIn(request):

    email = request.data.get('email')
    password = request.data.get('password')

    try:
        recruiter = Recruiter.objects.filter(user__email=email)

        if recruiter:

            if bcrypt.checkpw(bytes(password, 'utf-8'), recruiter[0].user.password.encode('utf-8')):

                payload_data = {
                    "id": recruiter[0].id,
                    "email": recruiter[0].user.email,
                    "type": recruiter[0].type,
                    "status": recruiter[0].status
                }
                token = jwt.encode(
                    payload=payload_data,
                    key='ami_rakib'
                )

                return Response({'token': token, 'payload_data': payload_data}, status=status.HTTP_200_OK)
            else:
                raise Exception('Invalid Password')

        else:
            raise Exception('Invalid Email')

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@custom_view_decorator
@api_view(['GET'])
def ViewAdmins(request):

    if request.curr_user.get('type') == 'admin':
        try:
            if Admin.objects.get(pk=request.curr_user.get('id')).status == 'manager':
                admnis = Admin.objects.exclude(status='manager')
                serializer = AdminSerializer(admnis, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'Only Manager can take action'}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@api_view(['GET'])
def ViewUsers(request):

    if request.curr_user.get('type') == 'admin':
        try:
            if Admin.objects.get(pk=request.curr_user.get('id')).status == 'manager':
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'Only Manager can take action'}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@api_view(['GET'])
def ViewStudents(request):

    if request.curr_user.get('type') == 'admin':

        try:
            if Admin.objects.get(pk=request.curr_user.get('id')).status == 'manager':
                students = Student.objects.select_related('user').all()
                serializer = StudentSerializer(students, many=True)
                return Response(serializer.data,  status=status.HTTP_200_OK)

            else:
                return Response({'error': 'Only Manager can take action'}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@api_view(['GET'])
def ViewRecruiters(request):

    if request.curr_user.get('type') == 'admin':
        try:
            students = Recruiter.objects.select_related('user').all()
            serializer = RecruiterSerializer(students, many=True)
            return Response(serializer.data,  status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def ViewCompanies(request):

    try:
        company = Company.objects.all()
        serializer = OnlyCompanySerializer(company, many=True)
        return Response(serializer.data,  status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@custom_view_decorator
@api_view(['DELETE'])
def DeleteUser(request, pk):

    if request.curr_user.get('type') == 'admin':
        try:
            if Admin.objects.get(pk=request.curr_user.get('id')).status == 'manager':
                User.objects.get(pk=pk).delete()
                return Response({'Deletion': 'Successfull'}, status=status.HTTP_202_ACCEPTED)

            else:
                return Response({'error': 'Only Manager can take action'}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@api_view(['DELETE'])
def DeleteStudent(request, pk):

    if request.curr_user.get('type') == 'admin':
        try:
            Student.objects.get(pk=pk).delete()
            return Response({'Deletion': 'Successfull'}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@api_view(['DELETE'])
def DeleteRecruiter(request, pk):

    if request.curr_user.get('type') == 'admin':
        try:
            Recruiter.objects.get(pk=pk).delete()
            return Response({'Deletion': 'Successfull'}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@api_view(['DELETE'])
def DeleteCompany(request, pk):

    if request.curr_user.get('type') == 'admin':
        try:
            Company.objects.get(pk=pk).delete()
            return Response({'Deletion': 'Successfull'}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@api_view(['DELETE'])
def DeleteJob(request, pk):

    if request.curr_user.get('type') == 'recruiter':
        try:
            Job.objects.get(pk=pk).delete()
            return Response({'Deletion': 'Successfull'}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@api_view(['GET'])
def RecruiterPending(request):

    if request.curr_user.get('type') == 'admin':
        try:
            recruiters = Recruiter.objects.filter(status="pending")
            serializer = RecruiterSerializer(recruiters, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@api_view(['GET'])
def RecruiterAccept(request):

    if request.curr_user.get('type') == 'admin':
        try:
            recruiters = Recruiter.objects.filter(status="accepted")
            serializer = RecruiterSerializer(recruiters, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@api_view(['GET'])
def RecruiterReject(request):

    if request.curr_user.get('type') == 'admin':
        try:
            recruiters = Recruiter.objects.filter(status="rejected")
            serializer = RecruiterSerializer(recruiters, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@api_view(['POST'])
def ChangeStatusAdmin(request, pk):

    if request.curr_user.get('type') == 'admin':

        try:
            statuss = request.data.get('status')

            if Admin.objects.get(pk=request.curr_user.get('id')).status == 'manager':
                admin = Admin.objects.get(pk=pk)
                admin.status = statuss
                admin.save()

                serializer = AdminSerializer(admin)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

            else:
                return Response({'error': 'Only Manager can take action'}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@api_view(['POST'])
def ChangeStatusRecruiter(request, pk):

    if request.curr_user.get('type') == 'admin':
        statuss = request.data.get('status')
        try:
            recruiter = Recruiter.objects.get(pk=pk)
            recruiter.status = statuss
            recruiter.save()

            serializer = RecruiterSerializer(recruiter)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@ api_view(['POST'])
def ChangeStatusJob(request, pk):

    if request.curr_user.get('type') == 'recruiter':

        statuss = request.data.get('status')
        try:
            job = Job.objects.get(pk=pk)
            job.status = statuss

            serializer = JobSerializer(job)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def ForgotPassword(request):

    email = request.data.get('email')

    try:
        user = User.objects.get(email=email)
        link = random.randint(0, 100000)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ChangePassword(request, link):

    email = request.data.get('email')
    password = request.data.get('password')
    if request.method == "POST" and link == 'oo':
        try:
            user = User.objects.get(email=email)
            user.password = password
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@custom_view_decorator
@api_view(['POST'])
def CreateJob(request):

    if request.curr_user.get('type') == 'recruiter':

        recruiter = Recruiter.objects.get(pk=request.curr_user.get('id'))
        company = Company.objects.get(recruiter=recruiter)

        if recruiter.status == 'accepted':

            title = request.data.get('title')
            description = request.data.get('description')
            experience = request.data.get('experience')
            skills = request.data.get('skills')
            location = request.data.get('location')
            salary = request.data.get('salary')
            end_date = request.data.get('end_date')
            yy = int(end_date[0])
            mm = int(end_date[1])
            dd = int(end_date[2])

            try:
                job = Job.objects.create(recruiter=recruiter, company=company, title=title, description=description, experience=experience, skills=skills,
                                         location=location,  salary=salary,  start_date=date.today(), end_date=date(yy, mm, dd))
                serializer = JobSerializer(job)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Recruiter needs to be accepted'}, status=status.HTTP_403_FORBIDDEN)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def ViewJobs(request):

    try:
        job = Job.objects.all()
        serializer = JobSerializer(job, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@custom_view_decorator
@api_view(['POST'])
def EditCompany(request, pk):

    if request.curr_user.get('type') == 'recruiter':

        if Recruiter.objects.get(pk=request.curr_user.get('id')).status == 'accepted':

            email = request.data.get('email')
            name = request.data.get('name')
            # logo = request.FILES.get('logo')
            description = request.data.get('description')
            type = request.data.get('type')

            try:
                company = Company.objects.get(pk=pk)
                company.email = email
                company.name = name
                company.description = description
                company.type = type
                company.save()

                serializer = OnlyCompanySerializer(company)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Recruiter needs to be accepted'}, status=status.HTTP_403_FORBIDDEN)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@ api_view(['POST'])
def EditJob(request, pk):

    if request.curr_user.get('type') == 'recruiter':

        if Recruiter.objects.get(pk=request.curr_user.get('id')).status == 'accepted':

            title = request.data.get('title')
            description = request.data.get('description')
            experience = request.data.get('experience')
            skills = request.data.get('skills')
            location = request.data.get('location')
            salary = request.data.get('salary')
            end_date = request.data.get('end_date')

            yy = int(end_date[0])
            mm = int(end_date[1])
            dd = int(end_date[2])

            try:
                job = Job.objects.get(pk=pk)
                job.title = title
                job.description = description
                job.experience = experience
                job.skills = skills
                job.location = location
                job.salary = salary
                job.end_date = date(yy, mm, dd)
                job.save()

                serializer = JobSerializer(job)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Recruiter needs to be accepted'}, status=status.HTTP_403_FORBIDDEN)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@ api_view(['GET'])
def AvailableJobs(request):

    if request.curr_user.get('type') == 'student':
        try:
            job = Job.objects.exclude(
                apply__student=Student.objects.get(pk=request.curr_user.get('id')))

            serializer = CompanyJobSerializer(job, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@ api_view(['GET'])
def StudentJobList(request):

    if request.curr_user.get('type') == 'student':
        try:
            student = Student.objects.get(pk=request.curr_user.get('id'))
            job = Job.objects.filter(apply__student=student)
            serializer = CompanyJobSerializer(job, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@ api_view(['GET'])
def RecruiterJobList(request):

    if request.curr_user.get('type') == 'recruiter':
        try:
            if Recruiter.objects.get(pk=request.curr_user.get('id')).status == 'accepted':
                recruiter = Recruiter.objects.get(
                    pk=request.curr_user.get('id'))
                job = Job.objects.filter(recruiter=recruiter)
                serializer = OnlyJobSerializer(job, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'Recruiter needs to be accepted'}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@ api_view(['GET'])
def JobDetail(request, pk):

    try:
        job = Job.objects.get(pk=pk)
        serializer = CompanyJobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@custom_view_decorator
@ api_view(['POST'])
def ApplyForJob(request, pk):

    if request.curr_user.get('type') == 'student':
        try:
            job = Job.objects.get(pk=pk)

            if job.status == 'open':
                student = Student.objects.get(pk=1)
                today = date.today()
                if job.end_date < today:
                    raise Exception('Sorry, submission date is over')
                else:
                    apply = Apply.objects.create(
                        job=job, student=student, applydate=date.today())
                    serializer = ApplySerializer(apply)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response({'error': 'Sorry, job is closed for applying'}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@ api_view(['GET'])
def ViewAppliedStudent(request, pk):

    if request.curr_user.get('type') == 'recruiter':
        try:
            job = Job.objects.get(pk=pk)
            applied = Apply.objects.filter(job=job)

            serializer = ApplyJobSerializer(applied, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@ api_view(['GET'])
def AppliedStudentDetails(request, pk):

    if request.curr_user.get('type') == 'recruiter':
        try:
            job = Job.objects.get(pk=pk)
            applied = Apply.objects.filter(job=job)

            serializer = ApplyJobSerializer(applied, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@ api_view(['GET'])
def AppliedStudentDetails(request, pk):

    if request.curr_user.get('type') == 'recruiter':

        try:
            applied = Apply.objects.get(pk=pk)

            serializer = ApplySerializer(applied)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)


@custom_view_decorator
@ api_view(['POST'])
def ChangeStatusApply(request, pk):

    if request.curr_user.get('type') == 'recruiter':
        statuss = request.data.get('status')

        try:
            applied = Apply.objects.get(pk=pk)

            applied.status = statuss
            applied.save()

            serializer = ApplyJobSerializer(applied)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Requested User is UNAUTHORIZED'}, status=status.HTTP_403_FORBIDDEN)
