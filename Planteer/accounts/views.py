from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def sign_up(request:HttpRequest):

    if request.method == "POST":
        try:
            new_user = User.objects.create_user(username=request.POST['username'],email=request.POST['email'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],password=request.POST['password'])
            new_user.save()
            messages.success(request, "User registered successfully", "alert-success")
            return redirect('accounts:sign_in')
        except Exception as e:
            print(e)
            messages.error(request, "Can't register user right now, please try again later", "alert-danger")

    return render(request, 'accounts/sign_up.html')

def sign_in(request:HttpRequest):

    if request.method =="POST":
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])

        if user:
            login(request, user)
            messages.success(request, "User logged in successfully", "alert-success")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Can't log in user, please try again", "alert-danger")

    return render(request, 'accounts/sign_in.html')

def log_out(request:HttpRequest):

    logout(request)
    messages.success(request, "User logged out successfully", "alert-success")

    return redirect(request.GET.get("next", "/"))