from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email  = request.POST.get('email')
        password  = request.POST.get('password1')
        repassword  = request.POST.get('password2')
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists.')
            return redirect('register')
        if password == repassword:
            new_user = User.objects.create_user(username=username , email=email , password=password)
            new_user.save()
            messages.success(request, 'User created successfully.')
            return redirect('login')
        else:
            messages.warning(request , 'Passwords didnt matched.')
            return redirect('register')

    return render(request , 'users/register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email , password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.warning(request , 'Email and password didnt matched.')
    return render(request , 'users/login.html')



def logout(request):
    auth.logout(request)
    messages.success(request , 'Logged out successfully.')
    return redirect('home')