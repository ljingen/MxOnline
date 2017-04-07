#coding:utf-8
'''
2017年4月7日
为了解决在1.10没有 patterns问题，进行了修改
'''
try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url

# from django import VERSION
# if VERSION[0:2]>(1,3):
#     from django.conf.urls import url
# else:
#     from django.conf.urls.defaults import patterns, url

from views import get_ueditor_controller

# urlpatterns = patterns('',
#     url(r'^controller/$',get_ueditor_controller)
# )
urlpatterns = [
    url(r'^controller/$', get_ueditor_controller)
]