from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    # image = models.FileField(null=True)
    mobile = models.IntegerField()
    gender = models.CharField(max_length=10,
                              choices=[('male', 'Male'), ('female', 'Female')])

    def _str_(self):
        return self.name, self.email,  self.mobile, self.gender,


class Admin(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='admin')
    status = models.CharField(max_length=10, default='none',
                              choices=[('none', 'None'), ('stuff', 'Stuff'), ('manager', 'Manager')])
    type = models.CharField(max_length=10, default='admin')

    def _str_(self):
        return self.user.name, self.status, self.type


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='student')
    # resume = models.FileField(null=True)
    type = models.CharField(max_length=10, default='student')

    def _str_(self):
        return self.user.name, self.type


class Recruiter(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='recruiter')
    status = models.CharField(max_length=15, default='pending', choices=[
        ('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    type = models.CharField(max_length=10, default='recruiter')

    def _str_(self):
        return self.user.name, self.status, self.type


class Company(models.Model):
    recruiter = models.ForeignKey(
        Recruiter, on_delete=models.CASCADE, related_name='company_recruiter')
    email = models.EmailField(max_length=20, unique=True)
    name = models.CharField(max_length=70)
    # logo = models.FileField(null=True, default='media/logo.webp')
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=20, default='business')
    status = models.CharField(max_length=10, default='running', choices=[
        ('running', 'Running'), ('closed', 'Closed')])

    def _str_(self):
        return self.recruiter.user.name, self.email, self.name, self.type, self.status


class Job(models.Model):
    recruiter = models.ForeignKey(
        Recruiter, on_delete=models.CASCADE, related_name='job_recruiter')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='job_company')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    experience = models.CharField(max_length=50)
    skills = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=15, default='open', choices=[
        ('open', 'Open'), ('closed', 'Closed')])

    def _str_(self):
        return self.recruiter.user.name, self.company.name, self.title, self.experience, self.skills, self.location, self.salary, self.status


class Apply(models.Model):
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='apply')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    applydate = models.DateField()
    status = models.CharField(max_length=25, default='pending', choices=[
        ('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Better Luck Next Time')])

    class Meta:
        unique_together = ['job', 'student']

    def _str_(self):
        return self.job.title, self.student.user.name, self.status
