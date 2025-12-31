from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Courses,Semester
from profile_app.models import Teacher,Student
from django.contrib.auth.models import User

# Create your views here.



@login_required(login_url='signin')
def BaseDashBoard(request):
    return render(request,"dashboard/basedashboard.html")
    
@login_required(login_url='signin')
def StudentDashBoard(request):
    return render(request,"dashboard/studentdashboard.html")


def TeacherDashBoard(request):
    return render(request,"dashboard/teacherdashboard.html")



def ViewCourses(request):
    courses=Courses.objects.all()
    if request.method=="POST":
        data=request.POST

        semester=data["semester"]

        if semester:
            seme=Semester.objects.filter(semester=semester).first()
            courses=seme.sem.all()
        
    
    paginator=Paginator(courses,5)
    page_number = request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,"features/viewcourses.html",{
      
        "page_obj":page_obj
    })


def ViewTeachers(request):

    teachers = Teacher.objects.select_related('user','user__profile_pic')
    return render(request,"features/viewteachers.html",{
        "teachers":teachers
    })



def ViewStudents(request):
    student_name=request.GET.get("q")
    if student_name:
        students=Student.objects.filter(user__username__icontains=student_name)
    else:
    #   students=Student.objects.select_related('user','user__profile_pic')
      students=Student.objects.all()
  
    return render(request,"features/viewstudents.html",{
        "students":students
    })

    