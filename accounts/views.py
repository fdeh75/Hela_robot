from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User

from Hela_robot.settings import STATIC_URL, STATIC_ROOT
from accounts.form import UserLoginForm, UserRegistrationForm, UserUpdateForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return render(request, 'accounts/register_done.html')
    return render(request, 'accounts/register.html', {'form': form})


def profile_view(request):
    if request.user.is_authenticated:
        user = request.user
        print(user.experience.all())
    #     if request.method == 'POST':
    #         form = UserUpdateForm(request.POST)
    #     else:
    #         form = UserUpdateForm(
    #             initial={'city': user.city,
    #                      'job_type': user.jobb_type,
    #                      'send_email': user.send_email})
    #         return render(request, 'accounts/profile_page.html', {'form': form})
    # else:
    #     return redirect('accounts:login')
    return render(request, 'accounts/profile_page.html', {'qs': user})

def profile_update_view(request):
    print(STATIC_ROOT)
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
        else:
            form = UserUpdateForm(
                initial={'city': user.city,
                         'job_type': user.jobb_type,
                         'send_email': user.send_email})
            return render(request, 'accounts/profile_page.html', {'form': form})
    else:
        return redirect('accounts:login')
    # return render(request, 'accounts/profile_page.html', {'qs': user})
