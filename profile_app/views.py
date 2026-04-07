from django.shortcuts import render,redirect
from .models import Student,Teacher,Profile
from dashboard.models import Semester
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
import re



def StudentRegistration(request):
    semesters = Semester.objects.all()

    if request.method == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        semester_id = request.POST.get("semester")

       
        password_regex = re.compile(
            r'^(?=.*[a-z])'       
            r'(?=.*[A-Z])'        
            r'(?=.*\d)'            
            r'(?=.*[@$!%*?&])'    
            r'.{8,}$'              
        )

        if not password_regex.match(password):
            messages.error(request,
                "Password must be at least 8 characters and include "
                "an uppercase letter, number, and special character (@$!%*?&)."
            )
            return redirect("sregister")
        

       
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect("sregister")

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=firstname,
            last_name=lastname
        )

        # Get Semester object
        semester = Semester.objects.get(id=semester_id)

        # Create Student
        Student.objects.create(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            user=user,
            semester=semester
        )

        return redirect("signin")

    return render(request, "registration/student.html", {
        "semesters": semesters
    })

def TeacherRegistration(request):
    if request.method=="POST":
        data=request.POST
        username=data["username"]
        firstname=data["firstname"]
        lastname=data["lastname"]
       
        password=data["password"]
        email=data["email"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect("tregister")
        password_regex = re.compile(
            r'^(?=.*[a-z])'       
            r'(?=.*[A-Z])'        
            r'(?=.*\d)'            
            r'(?=.*[@$!%*?&])'    
            r'.{8,}$'              
        )

        if not password_regex.match(password):
            messages.error(request,
                "Password must be at least 8 characters and include "
                "an uppercase letter, number, and special character (@$!%*?&)."
            )
            return redirect("sregister")
        

        user=User.objects.create_user(username=username,first_name=firstname,last_name=lastname,password=password,email=email)
        st=Teacher.objects.create(user=user)
        st.save()
        return redirect("signin")

    return render(request,"registration/teacher.html")


def ChoiceForRegistration(request):
    return render(request,"registration/choice.html")


def SignIn(request):
    if request.method=="POST":
        data=request.POST
        username=data["username"]
        password=data["password"]


        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect("signin")
        if hasattr(user,"student"):
            login(request,user)
            return redirect('studentdashboard')


        if hasattr(user,"teacher"):
            login(request,user)
            return redirect('teacherdashboard')
        else:
            return redirect("signin")
    return render(request,"signin/login.html")



def ProfileUpdate(request):
    if request.method=="POST":
        data=request.POST
        username=data["username"]
        firstname=data["firstname"]
        lastname=data["lastname"]
        email=data["email"]
        profileimage=request.FILES.get("profileimage")

        profile, created = Profile.objects.get_or_create(user=request.user)
        if profileimage:
            profile.profile_image = profileimage
            profile.save()

        if firstname:
            request.user.first_name=firstname
        if lastname:
            request.user.last_name=lastname
        if username:
            request.user.username=username
        if email:
            request.user.email=email
        request.user.save()
    return render(request,"updation/profileupdate.html")


def Logout(request):
    logout(request)
    return  redirect('signin')



@login_required(login_url='signin')
def ChangePassword(request):
    form=PasswordChangeForm(user=request.user)
    if request.method=="POST":
        data=request.POST
        form=PasswordChangeForm(user=request.user,data=data)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            return HttpResponse("hello")
    return render(request,"updation/changepassword.html",{
        "form":form
    })

