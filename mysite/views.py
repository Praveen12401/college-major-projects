from django.http import HttpResponse, HttpResponseRedirect
import openai, random, string
from django.shortcuts import render
from pytube import YouTube
from servise.models import Picture
from .forms import Userform, LoginForm
from django.contrib.auth import authenticate, login
# from django.core.mail import send_mail
from django.conf import settings

picturedata = Picture.objects.all()
data = {"picturedata": picturedata}


def index(request):
    print(settings.API)

    # subject = 'Subject of the email'
    # message = 'Body of the email.'
    # from_email = 'praveen264y@gamil.com'
    # recipient_list = ['praveenyadav16178@gmail.com']

    # send_mail(subject, message, from_email, recipient_list)
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def contant(requests):
    fn = Userform()
    data = {
        'email': fn
    }

    return render(requests, "contant.html", data)


def download(requests):
    return render(requests, "download.html")


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
        except:
            return "Someting is wrong please check internet connection"

    prompt = request.GET.get("prompt", "hi")

    assistant_reply = self_chat(prompt)

    return render(request, "chat_gpt.html", {"reply": assistant_reply, "question": prompt})


def single_video(request):
    if request.method == "GET":

        try:
            url = request.GET.get("url_of_video", "default")
            save_path = request.GET.get("path", "C:\\Users\\91638\\Downloads")

            str_1 = YouTube(url)

            title = str_1.title
            thumbnale = str_1.thumbnail_url

            data = {
                "title": title,
                "thumbnale": thumbnale,
                "internet": False

            }
            str = str_1.streams.get_highest_resolution()
            str.download(output_path=save_path)
        except:
            print("exception")
            data = {
                "title": "Something wrong",
                "thumbnale": False,
                "internet": True
            }
            return render(request, "download.html", data)

        return render(request, "download.html", data)
    print("last")

    return render(request, "download.html")


def user_login(request):
    form = LoginForm()
    capture1 = string.ascii_letters + string.digits
    capture = ' '.join(random.choice(capture1) for _ in range(5))
    print(capture)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse('Disable account')
            else:
                return HttpResponse('Invalid login')
        else:
            form = LoginForm()
        return render(request, 'account_login.html', {'form': form})
    return render(request, 'account_login.html', {'form': form, "capture": capture})
