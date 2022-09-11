from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin_signup', views.AdminSignUp),
    path('student_signup', views.StudentSignUp),
    path('recruiter_signup', views.RecruiterSignUp),
    path('create_company', views.CreateCompany),
    path('create_job', views.CreateJob),

    path('admin_login', views.AdminSignIn),
    path('student_login', views.StudentSignIn),
    path('recruiter_login', views.RecruiterSignIn),

    path('forgotPassword', views.ForgotPassword),
    path('change_password/<str:link>', views.ChangePassword),

    path('all_admins', views.ViewAdmins),
    path('all_users', views.ViewUsers),
    path('all_students', views.ViewStudents),
    path('all_recruiters', views.ViewRecruiters),
    path('all_companies', views.ViewCompanies),
    path('all_jobs', views.ViewJobs),

    path('edit_company/<int:pk>', views.EditCompany),
    path('edit_job/<int:pk>', views.EditJob),

    path('delete_user/<int:pk>', views.DeleteUser),
    path('delete_recruiter/<int:pk>', views.DeleteRecruiter),
    path('delete_company/<int:pk>', views.DeleteCompany),
    path('delete_job/<int:pk>', views.DeleteJob),

    path('recruiter_pending', views.RecruiterPending),
    path('recruiter_accepted', views.RecruiterAccept),
    path('recruiter_rejected', views.RecruiterReject),

    path('change_status/admin/<int:pk>',
         views.ChangeStatusAdmin),
    path('change_status/recruiter/<int:pk>',
         views.ChangeStatusRecruiter),
    path('change_status/job/<int:pk>', views.ChangeStatusJob),

    path('available_jobs', views.AvailableJobs),
    path('job_detail/<int:pk>', views.JobDetail),
    path('applyforjob/<int:pk>', views.ApplyForJob),

    path('applied_jobs', views.StudentJobList),

    path('created_jobs', views.RecruiterJobList),
    path('applied_student/<int:pk>', views.ViewAppliedStudent),
    path('applied_student_details/<int:pk>', views.AppliedStudentDetails),
    path('change_status/apply/<int:pk>', views.ChangeStatusApply),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
