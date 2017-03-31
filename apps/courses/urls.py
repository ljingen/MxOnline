# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView

urlpatterns = [
    #  课程列表页面
    url(r'^list/$', CourseListView.as_view(), name='courselist'),

    #  课程详情配置
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),

    #  课程详情配置
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),

    url(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name='course_comment'),

    #  在课程里面添加评论
    url(r'^add_comment/$', AddCommentsView.as_view(), name='add_comment'),

]
