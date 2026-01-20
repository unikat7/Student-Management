from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Courses
# Create your models here.


class Semester(models.Model):
    semester=models.IntegerField()
    def __str__(self):
        return self.semester


class Student(models.Model):
    username=models.CharField(max_length=50)
    firstname=models.CharField(max_length=50)
    email=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=20)
    semester=models.IntegerField()


    def __str__(self):
        return self.username

class Teacher(models.Model):
    email=models.CharField(max_length=30)
    username=models.CharField(max_length=50)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=30)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=30)
  

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile_pic")
    profile_image=models.ImageField(upload_to="profile_pic/")

    def __str__(self):
        return self.user.username




class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.student.username} - {self.course.course_name}"
