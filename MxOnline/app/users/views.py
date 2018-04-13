# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm
from utils.email_send import send_register_email

# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):

    @staticmethod
    def get(request):
        return render(request, "login.html", {})

    @staticmethod
    def post(request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", '')
            pass_word = request.POST.get("password", '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户账户或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class RegisterView(View):

    @staticmethod
    def get(request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    @staticmethod
    def post(request):

        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", '')
            is_register = UserProfile.objects.filter(username=user_name)
            for r in is_register:
                if r:
                    return render(request, "register.html", {"msg": "用户已注册",
                                                             'register_form': register_form})
            pass_word = request.POST.get("password", '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            if send_register_email(user_name, "register"):
                return render(request, "login.html")
            return render(request, "register.html", {'register_form': register_form})
        else:
            return render(request, "register.html", {"msg": "邮件发送失败，请联系管理员处理"})


class ActiveUserView(View):

    @staticmethod
    def get(request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.filter(email=email)
                user.is_active = True
                user.save()
        return render(request, "login.html")


class ForgetPasswordView(View):
    @staticmethod
    def get(request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {'forget_form': forget_form})

    @staticmethod
    def post(request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            user_name = request.POST.get("email", '')
            return render(request, "forgetpwd.html", {})

