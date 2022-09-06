from sqlite3 import Date
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from datetime import date
import random


@api_view(['GET', 'POST', 'DELETE'])
def ErrorPage(request):
    if request.method == 'POST' or 'GET' or 'DELETE':
        return Response({'not_found': 'Page Not Found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def AdminSignUp(request):

    if request.method == 'POST':
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        image = request.FILES.get('image')
        mobile = request.data.get('mobile')
        gender = request.data.get('gender')

        type = request.data.get('type')
        try:
            user = User.objects.create(
                name=name, email=email, password=password, image=image, mobile=mobile, gender=gender)

            admin = Admin.objects.create(
                user=user,  type=type)

            serializer = AdminSerializer(admin)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def StudentSignUp(request):

    if request.method == 'POST':
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        image = request.FILES.get('image')
        mobile = request.data.get('mobile')
        gender = request.data.get('gender')

        # resume = request.FILES.get('resume')
        try:
            user = User.objects.create(
                name=name, email=email, password=password, image=image, mobile=mobile, gender=gender)

            student = Student.objects.create(
                user=user)

            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def RecruiterSignUp(request):

    if request.method == 'POST':
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        image = request.FILES.get('image')
        mobile = request.data.get('mobile')
        gender = request.data.get('gender')

        try:
            user = User.objects.create(
                name=name, email=email, password=password, image=image, mobile=mobile, gender=gender)

            recruiter = Recruiter.objects.create(
                user=user)

            serializer = RecruiterSerializer(recruiter)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def CreateCompany(request, pk):

    if request.method == 'POST':
        email = request.data.get('email')
        name = request.data.get('name')
        # logo = request.FILES.get('logo')
        description = request.data.get('description')
        type = request.data.get('type')

        recruiter = request.objects.get(pk=pk)
        try:
            company = Company.objects.create(recruiter=recruiter,
                                             email=email, name=name,  description=description, type=type)

            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def AdminSignIn(request):

    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            admin = Admin.objects.filter(user__email=email)

            if admin:

                if admin[0].user.password == password:
                    serializer = AdminSerializer(admin, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise Exception('Invalid Password')

            else:
                raise Exception('Invalid Email')

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def StudentSignIn(request):

    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            student = Student.objects.filter(user__email=email)

            if student.exists():

                if student[0].user.password == password:
                    serializer = StudentSerializer(student, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise Exception('Invalid Password')

            else:
                raise Exception('Invalid Email')

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def RecruiterSignIn(request):

    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            recruiter = Recruiter.objects.filter(user__email=email)

            if recruiter:

                if recruiter[0].user.password == password:
                    serializer = RecruiterSerializer(recruiter, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise Exception('Invalid Password')

            else:
                raise Exception('Invalid Email')

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def SignOut(request):
#     logout(request)
#     return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def ViewAdmins(request):

    if request.method == 'GET':
        try:
            admnis = Admin.objects.exclude(status='manager')
            serializer = AdminSerializer(admnis, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ViewUsers(request):

    if request.method == 'GET':
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ViewStudents(request):
    print(request.error)

    if request.method == 'GET':
        try:
            students = User.objects.select_related('student').all()
            serializer = UserStudentSerializer(students, many=True)
            return Response(serializer.data,  status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ViewRecruiters(request):

    if request.method == 'GET':
        try:
            students = User.objects.select_related('recruiter').all()
            serializer = UserRecruiterSerializer(students, many=True)
            return Response(serializer.data,  status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ViewCompanies(request):

    if request.method == 'GET':
        try:
            company = Company.objects.all()
            serializer = RecruiterSerializer(company, many=True)
            return Response(serializer.data,  status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def DeleteUser(request, pk):

    if request.method == 'DELETE':
        try:
            User.objects.get(pk=pk).delete()
            return Response({'Deletion': 'Successfull'}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def DeleteStudent(request, pk):

    if request.method == 'DELETE':
        try:
            Student.objects.get(pk=pk).delete()
            return Response({'Deletion': 'Successfull'}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def DeleteRecruiter(request, pk):

    if request.method == 'DELETE':
        try:
            Recruiter.objects.get(pk=pk).delete()
            return Response({'Deletion': 'Successfull'}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def DeleteCompany(request, pk):

    if request.method == 'DELETE':
        try:
            Company.objects.get(pk=pk).delete()
            return Response({'Deletion': 'Successfull'}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def DeleteJob(request, pk):

    if request.method == 'DELETE':
        try:
            Job.objects.get(pk=pk).delete()
            return Response({'Deletion': 'Successfull'}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def RecruiterPending(request):

    if request.method == 'GET':
        try:
            recruiters = Recruiter.objects.filter(status="pending")
            serializer = RecruiterSerializer(recruiters, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def RecruiterAccept(request):

    if request.method == 'GET':
        try:
            recruiters = Recruiter.objects.filter(status="accepted")
            serializer = RecruiterSerializer(recruiters, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def RecruiterReject(request):

    if request.method == 'GET':
        try:
            recruiters = Recruiter.objects.filter(status="rejected")
            serializer = RecruiterSerializer(recruiters, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ChangeStatusAdmin(request, pk):

    if request.method == "POST":
        status = request.data.get('status')
        try:
            admin = Admin.objects.get(pk=pk)
            admin.status = status
            res = admin.save()

            serializer = AdminSerializer(res)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ChangeStatusRecruiter(request, pk):

    if request.method == "POST":
        status = request.data.get('status')
        try:
            recruiter = Recruiter.objects.get(pk=pk)
            recruiter.status = status
            res = recruiter.save()

            serializer = RecruiterSerializer(res)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['POST'])
def ChangeStatusJob(request, pk):

    if request.method == 'POST':

        status = request.data.get('status')

        try:
            job = Job.objects.get(pk=pk).update(
                end_date=date.today(), status=status)
            serializer = JobSerializer(job)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ForgotPassword(request):

    email = request.data.get('email')
    if request.method == "POST":
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
            res = user.save()
            serializer = UserSerializer(res)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def CreateJob(request):

    if request.method == 'POST':
        recruiter = request.data.get('recruiter')
        company = request.data.get('company')
        title = request.data.get('title')
        description = request.data.get('description')
        experience = request.data.get('experience')
        skills = request.data.get('skills')
        location = request.data.get('location')
        salary = request.data.get('salary')
        end_date = request.data.get('end_date')
        status = request.data.get('status')

        try:
            job = Job.objects.create(recruiter=recruiter, company=company, title=title, description=description, experience=experience, skills=skills,
                                     location=location,  salary=salary,  start_date=date.today(), end_date=end_date, status=status)
            serializer = JobSerializer(job)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ViewJobs(request):

    if request.method == "GET":
        try:
            job = Job.objects.all()
            serializer = JobSerializer(job, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def EditCompany(request, pk):

    if request.method == 'POST':
        email = request.data.get('email')
        name = request.data.get('name')
        # logo = request.FILES.get('logo')
        description = request.data.get('description')
        type = request.data.get('type')

        try:
            company = Company.objects.get(pk=pk).update(
                email=email, name=name,  description=description, type=type)

            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['POST'])
def EditJob(request, pk):

    if request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        experience = request.data.get('experience')
        skills = request.data.get('skills')
        location = request.data.get('location')
        salary = request.data.get('salary')
        end_date = request.data.get('end_date')
        status = request.data.get('status')

        try:
            job = Job.objects.get(pk=pk).update(title=title, description=description, experience=experience, skills=skills,
                                                location=location,  salary=salary, end_date=end_date, status=status)
            serializer = JobSerializer(job)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET'])
def AvailableJobs(request):

    if request.method == "GET":
        try:
            job = Job.objects.select_related(
                'apply').filter(apply__student=None)

            serializer = JobSerializer(job, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET'])
def StudentJobList(request):

    if request.method == "GET":
        try:
            student = Student.objects.get(pk=1)
            applied = Apply.objects.filter(student=student)
            serializer = ApplySerializer(applied, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET'])
def RecruiterJobList(request):

    if request.method == "GET":
        try:
            recruiter = Recruiter.objects.get(pk=1)
            job = Job.objects.filter(recruiter=recruiter)
            serializer = JobSerializer(job, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET'])
def JobDetail(request, pk):

    if request.method == "GET":
        try:
            job = Job.objects.get(pk=pk)
            serializer = JobSerializer(job)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['POST'])
def ApplyForJob(request, pk):

    if request.method == "POST":
        try:
            job = Job.objects.get(pk=pk)
            student = Student.objects.get(pk=1)
            today = date.today()
            if job.end_date < today:
                raise Exception('Sorry, submission date over')
            else:
                apply = Apply.objects.create(
                    job=job, student=student, applydate=date.today())
                serializer = ApplySerializer(apply)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET'])
def ViewAppliedStudent(request, pk):

    if request.method == "GET":
        try:
            job = Job.objects.get(pk=pk)
            applied = Apply.objects.get(job=job)

            serializer = ApplySerializer(applied, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['POST'])
def ChangeStatusApply(request, pk):

    if request.method == "POST":
        status = request.data.get('status')

        try:
            applied = Apply.objects.get(pk=pk)
            applied.status = status
            res = applied.save()

            serializer = ApplySerializer(res, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
