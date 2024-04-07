from django.http import HttpResponse, HttpResponseRedirect

import openai, os
from django.shortcuts import render, redirect
from pytube import YouTube
from servise.models import Project
from .forms import Userform, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import FileResponse
from django.conf import settings


# from django.conf import settings


def index(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    projectdata = Project.objects.all()
    data = {"projectdata": projectdata}
    for item in projectdata:
        print(item.project_file.path)

    return render(request, "contact.html", data)




def chat_gpt(request):
    return render(request, "chat_gpt.html")


def chat_gpt_work(request):
    # Set your OpenAI API key
    api_key = "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"
    # Initialize the OpenAI API client
    openai.api_key = api_key

    # Create a conversation with a system message
    def self_chat(prompt):

        try:

            # Create a conversation with a system message
            conversation = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]

            # Generate a response from GPT-3
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation,
            )
            # Extract and return the assistant's reply
            assistant_reply = response['choices'][0]['message']['content']
            return assistant_reply
        except Exception as e:
            return f"Someting is wrong please check internet connection{e}"

    prompt = request.GET.get("prompt", "hi")

    assistant_reply = self_chat(prompt)

    return render(request, "chat_gpt.html", {"reply": assistant_reply, "question": prompt})


url = ''
save_path = ''
str_1 = ''


def download(request):
    global url
    global save_path
    global str_1

    if request.method == "POST":
        item = []
        itemv = []

        try:
            url = request.POST.get("url_of_video", "default")
            save_path = request.POST.get("path", "C:\\Users\\91638\\Downloads")

            str_1 = YouTube(url)
            s = str_1.streams.get_highest_resolution()

            title = str_1.title
            thumbnale = str_1.thumbnail_url
            '''  '''
            total = s.filesize
            video_size = total // 1048576

            print('size', total // 1024, ' KB')
            print('size mb', total // 1048576, 'MB')

            # Get all streams (progressive and audio)
            all_streams = str_1.streams
           
            data = {
                "title": title,
                "thumbnale": thumbnale,
                'video_size': f'{video_size}MB', 
                "internet": False,
                'downlode': True,
                'item': item,
                'itemv': itemv,
                'video': 'Get video'

            }
            # str = str_1.streams.get_highest_resolution()
            # str.download(output_path=save_path)
        except:
            print("exception")
            data = {
                "title": "Something wrong",
                "thumbnale": False,
                "internet": True
            }
            return render(request, "download.html", data)

        return render(request, "download.html", data)

    return render(request, "download.html")


def single_video(request):
    if request.method == "GET":

        try:
            print('downloding now....')

            str = str_1.streams.get_highest_resolution()
            file_path=str.download()
            print('file path',file_path)
        

            file_name = os.path.basename(file_path)
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                return response
        except:
            print("exception")
            data = {
                "title": "Something wrong",
                "thumbnale": False,
                "internet": True
            }
            return render(request, "download.html", data)

        return HttpResponseRedirect('/download/')
    print("last")

    return render(request, "download.html")


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
        if len(username) > 10:
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
            messages.success(request, f" Your iCoder has been unsuccessfully createe Account  username exist '{username}' try different name")
            return redirect('Home')




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
