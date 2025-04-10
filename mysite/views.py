from django.http import HttpResponse, HttpResponseRedirect

# import os, yt_dlp
from django.shortcuts import render, redirect

from servise.models import Project
from .forms import Userform, LoginForm
from django.contrib.auth import authenticate, login, logout
# from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import FileResponse
from django.conf import settings


# from django.conf import settings


def index(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def service(request):
    projectdata = Project.objects.all()
    data = {"projectdata": projectdata}
    for item in projectdata:
        print(item.project_file.path)

    return render(request, "service.html", data)



def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) > 20:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('Home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('Home')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('Home')

        # Create the user

        try:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            login(request, myuser)
            messages.success(request, " Your iCoder has been successfully created and Logged in")
            return redirect('Home')

        except Exception as e:
            messages.success(request,
                             f" Your iCoder has been unsuccessfully createe Account  username already exist '{username}' try different name")
            return redirect('handleSignUp')




    else:
        return HttpResponse("404 - Not found")


def handeLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("Home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("Home")

    return HttpResponse("404- Not found")

    return HttpResponse("login")


def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('Home')
