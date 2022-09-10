from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(Company)
admin.site.register(Recruiter)
admin.site.register(Job)
admin.site.register(Apply)
admin.site.register(ForgotPasswordLink)
