from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.contrib import messages
from .models import Profile

# Create your views here.

def sign_up(request:HttpRequest):

    if request.method == "POST":
        try:
            with transaction.atomic():
                new_user = User.objects.create_user(username=request.POST['username'],email=request.POST['email'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],password=request.POST['password'])
                new_user.save()

                profile = Profile(user = new_user, about = request.POST['about'], profile_image = request.FILES.get('profile_image', Profile.profile_image.field.get_default()))
                profile.save()

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

def user_profile(request:HttpRequest,user_name):
    try:
        user = User.objects.get(username = user_name)
        if not Profile.objects.filter(user=user).first():
            new_profile = Profile(user=user)
            new_profile.save()
        profile = user.profile
    except:
        return
    
    return render (request, 'accounts/profile.html', {'user':user})

def update_user_profile(request:HttpRequest):

    if not request.user.is_authenticated:
        messages.warning(request, "Only registered users can update their profile", "alert-warning")
        return redirect("accounts:sign_in")
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                        user:User = request.user

                        user.first_name = request.POST["first_name"]
                        user.last_name = request.POST["last_name"]
                        user.email = request.POST["email"]
                        user.save()

                        profile:Profile = user.profile
                        profile.about = request.POST["about"]
                        profile.profile_image = request.FILES.get('profile_image', profile.profile_image)
                        profile.save()

                        messages.success(request, "updated profile successfuly", "alert-success")
        except Exception as e:
            messages.error(request, "Couldn't update profile", "alert-danger")
            print(e)
        
    
    return render(request, 'accounts/update_profile.html')