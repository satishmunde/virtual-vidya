from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'home/home.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return render(request, 'login/login.html')

def register(request):
    return render(request, 'signup/signup.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    return render(request, 'dashboard/dashboard.html')