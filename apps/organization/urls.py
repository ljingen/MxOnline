# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from .views import OrgListView, AddUserAskView, OrgHomeView, OrgCourseView, OrgTeacherView, OrgDescView, AddFavView
from .views import TeacherListView, TeacherDetailView
urlpatterns = [
    url(r'^list/$', OrgListView.as_view(), name='orglist'),
    url(r'user_ask/$', AddUserAskView.as_view(), name='user_ask'),
    url(r'org_home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),
    #  添加收藏的处理功能
    url(r'add_fav/$', AddFavView.as_view(), name='add_fav'),

    #  添加教师的列表
    url(r'teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    #  添加教师详情页
    url(r'teacher/list/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),

]
