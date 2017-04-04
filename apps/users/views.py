# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View

from users.models import UserProfile, EmailVerifyRecord
from users.forms import LoginFrom, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            '''从post中获取到emal和password的值'''
            user_name = request.POST.get('email', '')
            '''用户是否注册'''
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在'})
            pass_word = request.POST.get('password', '')
            '''实例化一个UserProfile对象'''
            user_profile = UserProfile()

            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            '''将用户注册信息保存到数据库'''
            user_profile.save()
            '''发送认证邮件'''
            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form, 'msg':'用户已存在'})


class ActiveView(View):

    def get(self, request, active_code):
        all_codes = EmailVerifyRecord.objects.filter(code=active_code)
        user = UserProfile()
        if all_codes:
            for recode in all_codes:
                email = recode.email
                user = UserProfile.objects.get(email=email)
                user.is_active =True
                user.save()
            return render(request, 'login.html', {'msg': '已经激活成功，请登陆','login_form': user})
        else:
            '''还没做'''
            return render(request, 'active_fail.html', {})
        return render(request,'login.html', {})


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_from = LoginFrom(request.POST)
        if login_from.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '账号未激活,请进入邮箱激活账户!','login_from':login_from} )
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误,请重试!'})
        else:
            print 'hello'
            return render(request, 'login.html', {'login_form': login_from})


class ForgetPwdView(View):

    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            '''发送找回密码的邮件'''
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg': '表格信息错误'})


class ResetView(View):

    def get(self, request, reset_code):
        all_codes = EmailVerifyRecord.objects.filter(code=reset_code)
        user = UserProfile()
        if all_codes:
            for recode in all_codes:
                email = recode.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            '''还没做'''
            return render(request, 'active_fail.html', {})
        return render(request,'login.html', {})


class ModifyPwdView(View):
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'modifypwd_form': modifypwd_form, 'email': email, 'msg': '密码不一致!'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html', {'msg': '密码已经修改,请用新密码登录'})
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'modifypwd_form': modifypwd_form, 'email': email, 'msg': '信息错误,请重试!'})


class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人中心处理view
    """
    def get(self, request):
        return  render(request, 'usercenter-info.html', {})
