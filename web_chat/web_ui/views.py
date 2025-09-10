import json
import os
import re

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import (
    CustomLoginForm,
    CustomPasswordResetForm,
    CustomPasswordResetSentMailForm,
    CustomUserCreationForm,
)
from .models import CustomUsersModel


# Create your views here.
def user_login(request):
    if request.method == "POST":
        login_form = CustomLoginForm(request=request, data=request.POST)
        print(f"form data: {login_form.data}")
        print(f"form errors: {login_form.errors}")
        print("isform valid: ", login_form.is_valid())
        if login_form.is_valid():
            email = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            print(f"Email: {email}, Password: {password}")
            try:
                user = authenticate(request=request, username=email, password=password)
            except ValueError as e:
                print(f"Error: {e}")
                user = None
            if user is not None:
                login(request=request, user=user)
                messages.success(request=request, message="Login Successfull")
                next_url = request.GET.get("next", "dashboard")
                send_mail(
                    "Login Successfull to Django Project",
                    "You have successfully logged in to Django Project",
                    "siva9963365904@gmail.com",
                    [request.user],
                )
                if next_url:
                    return redirect(next_url)
                return redirect("home")  # dashboard
                # return redirect("/user/1/")  # dashboard
            else:
                messages.error(request=request, message="Invalid Email or Password")
                raise ValueError("Invalid Email or Password")
    else:
        return render(request=request, template_name="login.html")


@login_required
def home(request):
    """function to render home page"""
    print(request.method)
    if request.method == "POST":
        return HttpResponse("Invalid Email")
    else:
        return render(request, template_name="home.html")


def create_user(request):
    if request.method == "POST":
        print(request.POST)
        form = CustomUserCreationForm(request.POST)
        print("***********Form is not valid***********")
        if form.is_valid():
            print("***********Form is valid***********")
            user = form.save()
            login(request=request, user=user)
            messages.success(request=request, message="Registration Successfull")
            return redirect("login_user")
        else:
            print(form.errors)
            messages.error(request=request, message="Form is Not Valid")
            return render(request=request, template_name="register.html")
    else:
        return render(request=request, template_name="register.html")


def reset_password(request):
    """function to reset password"""
    print(request.method)
    if request.method == "POST":
        return HttpResponse("Invalid Email")
    else:
        return render(request, template_name="password_reset_email.html")


def password_reset_mail(request):
    """function to reset password"""
    print(request.method)
    if request.method == "POST":
        form = CustomPasswordResetSentMailForm(request.POST)
        print("isform valid: ", form.is_valid())
        print(form.errors)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            print(f"Email: {email}")
            try:
                user = CustomUsersModel.objects.get(email=email)
            except CustomUsersModel.DoesNotExist:
                user = None
            print(f"User: {user}")
            if user is not None:
                messages.success(request=request, message="Email Exists")
                # send mail
                print(user)
                print(f"user_pk token: {default_token_generator.make_token(user)}")
                context = {
                    "user": user,
                    "domain": request.META["HTTP_HOST"],
                    "site_name": "Django Project",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                    "protocol": "http",
                }
                form.send_mail(
                    subject="mail_subject.html",
                    email_template_name="password_reset_mail_body.html",
                    context=context,
                    from_email="siva.nuttakki@gmail.com",
                    to_email=email,  # user.email
                )
                messages.success(request=request, message="Mail Sent Successfully")
                return redirect("login_user")


def password_reset_confirm(request, uidb64, token):
    """function to reset password"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        user = CustomUsersModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUsersModel.DoesNotExist):
        user = None
    print(f"User password confirm: {user}")
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            print("POST Method")
            form = CustomPasswordResetForm(user, request.POST)
            print("isform valid: ", form.is_valid())
            print(form.errors)
            if form.is_valid():
                new_password = form.cleaned_data.get("new_password1")
                print(f"New Password: {new_password}")
                user.set_password(new_password)
                user.save()
                messages.success(
                    request=request, message="Password Updated Successfully"
                )
                return redirect("login_user")
        else:
            form = CustomPasswordResetForm(user)
            return render(
                request,
                "password_reset_confirm.html",
                {
                    "domain": request.META["HTTP_HOST"],
                    "uid": uidb64,
                    "token": token,
                    "protocol": "http" if os.getenv("ENV") == "local" else "https",
                },
            )
    else:
        return render(request, "password_reset_confirm.html")


@login_required
def user_chat(request):
    """function to render user chat page"""
    if request.method == "GET":
        print(f"User id: {request.user.pk}")
        fetch_contacts_url = (
            f"http://localhost:8000/user_contacts?user_id={request.user.user_id}"
        )
        print(f"Fetch Contacts URL: {fetch_contacts_url}")
        response = requests.get(fetch_contacts_url)
        response_details = json.loads(response.text)
        print(f"Response details: {response_details}")
        if response.status_code == 404:
            response_details = []

        return render(
            request,
            template_name="chat_app.html",
            context={
                "contacts": response_details,
                "current_user_id": request.user.pk,
                "current_user_email": request.user.email,
                "current_user_mobile": request.user.mobile,  # Add this line
            },
        )  # user_chat.html

    return HttpResponse("Invalid Email")


@login_required
def add_contact(request):
    """function to add a contact"""
    if request.method == "POST":
        contact_email = request.POST.get("contact_email")
        print(f"Contact Email: {contact_email}")
    return HttpResponse("Contact Added Successfully")


def message(request, user_id):
    """function to render user chat page"""
    if request.method == "GET":
        fetch_contacts_url = (
            f"http://localhost:8000/user_contacts?user_id={request.user.user_id}"
        )
        print(f"Fetch Contacts URL: {fetch_contacts_url}")
        response = requests.get(fetch_contacts_url)
        response_details = json.loads(response.text)
        print(f"Response details: {response_details}")
        if response.status_code == 404:
            response_details = []

        return render(
            request,
            template_name="chat_app.html",
            context={
                "contacts": response_details,
                "current_user_id": request.user.pk,
                "current_user_email": request.user.email,
                "current_user_mobile": request.user.mobile,  # Add this line
            },
        )  # user_chat.html
