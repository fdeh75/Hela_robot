from django.shortcuts import render
from django.contrib.auth import authenticate, login

from accounts.form import UserLoginForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get