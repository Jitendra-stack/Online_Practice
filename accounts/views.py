from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Register User
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')  # Added
        last_name = request.POST.get('last_name', '')  # Added

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            messages.info(request, 'User with this username already exists')
            return redirect("/auth/register/")
        
        # Create a new user
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        user.save()
        
        messages.info(request, 'User created successfully')
        return redirect('/auth/login/')
    
    template = loader.get_template('register.html')
    return HttpResponse(template.render({}, request))

# Login User
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, 'User with this username does not exist')
            return redirect('/auth/login/')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.info(request, 'Invalid password')
            return redirect('/auth/login/')
        
        login(request, user)
        messages.info(request, 'Login successful')
        return redirect('/auth/profile/')
    
    template = loader.get_template('login.html')
    return HttpResponse(template.render({}, request))

# Logout User
def logout_user(request):
    logout(request)
    return redirect('/auth/login/')

# Profile User (Fixed)
@login_required
def profile_user(request):
    user = request.user
    
    full_name = f"{user.first_name} {user.last_name}".strip() if user.first_name or user.last_name else "N/A"
    joined_on = user.date_joined.strftime('%B %d, %Y') if hasattr(user, 'date_joined') else "Unknown"

    template = loader.get_template('profile.html')
    context = {
        'user': user,
        'full_name': full_name,
        'joined_on': joined_on
    }

    return HttpResponse(template.render(context, request))
