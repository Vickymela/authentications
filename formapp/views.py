from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from .helpers import *
import random


def Home(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    else:
      return render(request, 'index.html')

def RegisterView(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Basic validation
        if not username or not email or not password:
            messages.error(request, "All fields are required")
            return redirect('register')

        user_data_has_error = False

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "Username already exists")

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already exists")

        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, "Password must be at least 5 characters")

        if user_data_has_error:
            return redirect('register')

        # Create new user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created. Login now!")
        return redirect('login')

    return render(request, 'signupdj.html')


def LoginView(request):

    print('login hit')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username).first()

        

        #user = authenticate(request, username=username, password=password)

        

        if user is not None and user.check_password(password):
            login(request, user)

            return redirect('home')
        
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'logindj.html')

def LogoutView(request):

    logout(request)

    return redirect('login')

def ForgotPassword(request):

    print('hit: forgot password')
    print(request)

    if request.method == "POST":
        email = request.POST.get("email")

        # FIX: correct query
        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, 'User not found')
            return render(request, "forgotpassword.html")

        code = generate_otp(user)

        if code:
            email_body = f'Your OTP code is {code}'

            email_message = EmailMessage(
                'Reset your password',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]
            )
            email_message.send()   # SEND EMAIL (You forgot this)

            messages.success(request, 'OTP sent successfully')
            return redirect("verify_otp")

    return render(request, "forgotpassword.html")

def verify_otp(request):
    print('hit : otp verification')

    if request.method == "GET":
        return render(request, 'verify_otp.html')

    code = request.POST.get('otp')
    email = request.POST.get('email')

    user = User.objects.filter(email=email).first()

    if not user:
        messages.error(request, "User not found")
        return render(request, 'verify_otp.html')

    feedback = Verify_otp(user, code)  # your helper

    if not feedback:  # OTP FAILED
        messages.error(request, "OTP verification failed")
        return render(request, 'verify_otp.html')

    # OTP SUCCESS → redirect with user ID
    return redirect('reset-password', reset_id=user.id)


def ResetPassword(request, reset_id):
    print("hit password reset")

    # Make sure user exists
    try:
        user = User.objects.get(id=reset_id)
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect("forgot-password")

    if request.method == "GET":
        return render(request, "reset.html", {"reset_id": reset_id})

    if request.method == "POST":
        newpassword = request.POST.get('new_password')
        confirmpassword = request.POST.get('confirm_password')

        if newpassword != confirmpassword:
            messages.error(request, "Passwords must match")
            return redirect('reset-password', reset_id=reset_id)

       
        user.set_password(newpassword)
        user.save()

        messages.success(request, "Password reset successful! You can now login.")
        return redirect("login")
