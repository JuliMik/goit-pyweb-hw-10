from django.utils import timezone
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import RegisterForm, LoginForm


# Функція реєстрації нового користувача
def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='app_quotes:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Не зберігаємо ще користувача
            user.last_login = timezone.now()  # Встановлюємо значення last_login
            user.save()  # Тепер зберігаємо користувача в базу даних

            return redirect(to='app_quotes:main')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})


# Функція входу
def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='app_quotes:main')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='app_quotes:main')

    return render(request, 'users/login.html', context={"form": LoginForm()})


# Функція виходу з акаунту
@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='app_quotes:main')
