from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import UserProfile
from .forms import SignupForm, UserProfileForm
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_anonymous:
        return redirect("/login/")
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'index.html', {'profile': user_profile})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Trying to authenticate user: {username}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("User authenticated successfully")
            auth_login(request, user)
            return redirect("/")  # Redirect to home page after successful login
        else:
            print("Authentication failed")
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def user_logout(request):
    auth_logout(request)
    return redirect("/login/")

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            auth_login(request, user)
            return redirect('/')  # Redirect to home page after signup
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def update_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'update_profile.html', {'form': form})
