# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.conf.urls import url

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 引入分页器


from users.models import UserProfile, EmailVerifyRecord, Banner
from users.forms import LoginFrom, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfo
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course

# Create your views here.


class CustomBackend(ModelBackend):
    """
    custom the login backend,
    overrite the authenticate method()
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            """验证username或者email"""
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    """
    user register the system
    get():
    post():
    """
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
            '''发送注册成功的消息信息'''
            message = UserMessage()
            message.message = "欢迎注册成功暮学在线网"
            message.user = user_profile.id
            message.save()
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


class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


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
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '账号未激活,请进入邮箱激活账户!','login_from':login_from} )
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误,请重试!'})
        else:
            print ('hello')
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
    """
    未登录时修改用户的密码
    """
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
        currentpage = 'info'
        return render(request, 'usercenter-info.html', {'currentpage':currentpage})

    def post(self,request):
        userinfo_form = UserInfo(request.POST, instance=request.user)
        if userinfo_form.is_valid():
            userinfo_form.save()
            return HttpResponse('{"status": "success","msg":"添加成功","name":"金刚狼"}', content_type='application/json')

        else:
            return HttpResponse('{"status": "fail","msg":"添加出错了","name":"金刚狼"}', content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户上传图片程序
    """
    def post(self, request):
        upload_image_form = UploadImageForm(request.POST, request.FILES)
        if upload_image_form.is_valid():
            image = upload_image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse('{"status": "fail","msg":"添加出错了","name":"金刚狼"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status": "fail","msg":"密码不一致","name":"金刚狼"}', content_type='application/json')
            request.user.password = make_password(pwd1)
            request.user.save()
            return HttpResponse('{"status": "success","msg":"修改成功","name":"金刚狼"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modifypwd_form.errors), content_type='application/json')


class SendMailCodeView(LoginRequiredMixin, View):
    """
    发送邮件验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')
        exit_email = UserProfile.objects.filter(email=email)
        if exit_email:
            return HttpResponse('{"email": "邮箱已经存在"}', content_type='application/json')
        '''发送认证邮件'''
        send_register_email(email, 'update')
        return HttpResponse('{"status": "success","msg":"修改成功","name":"金刚狼"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    个人中心更改用户的邮箱
    """
    def post(self,request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        exit_code = EmailVerifyRecord.objects.filter(code=code, send_type='update', email=email)
        if exit_code:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success","msg":"修改成功","name":"金刚狼"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """
    def get(self, request):
        currentpage = 'course'
        all_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'all_courses': all_courses,
            'currentpage':currentpage})


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我收藏的课程机构
    """
    def get(self, request):
        currentpage = 'favorite'
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type='2')
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
            'currentpage': currentpage})


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我收藏的教师
    """
    def get(self, request):
        currentpage = 'favorite'
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type='3')
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
            'currentpage':currentpage})


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我收藏的课程机构
    """
    def get(self, request):
        currentpage = 'favorite'
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type='1')
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
            'currentpage': currentpage})


class MyMessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):

        currentpage = 'message'

        all_messages = UserMessage.objects.filter(user=request.user.id)
        '''处理页面分页'''
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = 1
        paginator = Paginator(all_messages, 5, request=request)  # 获取一共有多少个页面
        all_message = paginator.page(page)  # 拿到指定的分页

        return render(request, 'usercenter-message.html', {'all_message': all_message,
                                                           'currentpage': currentpage})


class IndexView(View):
    '''
    暮学在线网首页视图
    '''
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        courses =Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs
        })

        '''
        全局处理404出错页面的函数
        '''

def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response

def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
