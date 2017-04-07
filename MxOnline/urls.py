# -*- coding: utf-8 -*-
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin
import extra_apps.DjangoUeditor

# from users.views import user_login
from users.views import LoginView, LogoutView, RegisterView, ActiveView, ForgetPwdView, ResetView, ModifyPwdView
from organization.views import OrgListView
from users.views import IndexView
from MxOnline.settings import MEDIA_ROOT
xadmin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    url(r'xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<active_code>[-\w]+)/$', ActiveView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget'),
    url(r'^reset/(?P<reset_code>[-\w]+)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    # 机构 列表的url配置
    url(r'^org/', include('organization.urls', namespace='org')),
    # 课程 列表的url配置
    url(r'^course/', include('courses.urls', namespace='course')),
    # 用户 列表的url配置
    url(r'^users/', include('users.urls', namespace='users')),
    #  配置django Ueditor的编辑器
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    # 配置如何在html页面里面去加载静态的media文件
    url(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
    # 配置如何在生产环境配置static
    # url(r'^static/(?P<path>.*)/$', serve, {'document_root': STATIC_ROOT}),
]

#配置全局404页面处理
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'

