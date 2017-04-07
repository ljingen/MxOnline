# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from .views import UserinfoView, UploadImageView, UpdatePwdView
from .views import SendMailCodeView, UpdateEmailView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView
from .views import MyMessageView
urlpatterns = [
    #  用户个人中心页面
    url(r'^info/$', UserinfoView.as_view(), name='user_info'),
    #  用户修改头像的url
    url(r'^image/updaload/$', UploadImageView.as_view(), name='image_upload'),
    #  个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    #  发送邮箱验证码
    url(r'^sendemail_code/$', SendMailCodeView.as_view(), name='sendmail_code'),
    #  修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    # 我的收藏机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),
    # 我的收藏老师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
    # 我的收藏课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),
    # 我的收藏课程
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),
]
