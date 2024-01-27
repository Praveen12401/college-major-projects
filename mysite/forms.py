from django import forms


class Userform(forms.Form):
    Name = forms.CharField()
    Branch = forms.CharField()
    Smester = forms.IntegerField()
    email = forms.EmailField()
    age = forms.DateField()


''' create a login form here class'''


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
