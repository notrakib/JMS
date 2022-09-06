from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_signup', views.AdminSignUp),
    path('student_signup', views.StudentSignUp),
    path('recruiter_signup', views.RecruiterSignUp),
    path('create_company', views.CreateCompany),  # Recruiter
    path('create_job', views.CreateJob),  # Recruiter

    path('admin_login', views.AdminSignIn),
    path('student_login', views.StudentSignIn),
    path('recruiter_login', views.RecruiterSignIn),

    # path('Logout', views.SignOut),
    path('ForgotPassword', views.ForgotPassword),
    path('change_password', views.ChangePassword),

    path('all_admins', views.ViewAdmins),  # Manager
    path('all_users', views.ViewUsers),  # Manager
    path('all_students', views.ViewStudents),  # Manager
    path('all_recruiters', views.ViewRecruiters),  # Stuff
    path('all_companies', views.ViewCompanies),
    path('all_jobs', views.ViewJobs),

    path('edit_company/<int:pk>', views.EditCompany),  # Recruiter
    path('edit_job/<int:pk>', views.EditJob),  # Recruiter

    path('delete_user/<int:pk>', views.DeleteUser),  # Manager
    path('delete_recruiter/<int:pk>', views.DeleteRecruiter),  # Stuff
    path('delete_company/<int:pk>', views.DeleteCompany),  # Stuff
    path('delete_job/<int:pk>', views.DeleteJob),  # Recruiter

    path('recruiter_pending', views.RecruiterPending),  # Stuff
    path('recruiter_accepted', views.RecruiterAccept),  # Stuff
    path('recruiter_rejected', views.RecruiterReject),  # Stuff

    path('change_status/admin/<int:pk>',
         views.ChangeStatusAdmin),  # Stuff
    path('change_status/recruiter/<int:pk>',
         views.ChangeStatusRecruiter),  # Stuff
    path('change_status/job/<int:pk>', views.ChangeStatusJob),  # Recruiter

    path('available_jobs', views.AvailableJobs),
    path('job_detail/<int:pk>', views.JobDetail),
    path('applyforjob/<int:pk>', views.ApplyForJob),  # Student

    path('applied_jobs', views.StudentJobList),  # Student

    path('created_jobs', views.RecruiterJobList),  # Recruiter
    path('applied_student/<int:pk>', views.ViewAppliedStudent),  # Recruiter
    path('change_status/apply/<int:pk>', views.ChangeStatusApply),  # Recruiter

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
