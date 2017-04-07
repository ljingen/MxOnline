# -*- coding: utf-8 -*-
import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from .models import UserProfile, EmailVerifyRecord, Banner
from django.contrib.auth.models import User


class UserProfileAdmin(UserAdmin):
    pass


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "慕学网后台管理系统"
    site_footer = "慕学在线网"
    menu_style = "accordion"


# class UserProfileAdmin(object):
#     list_display = ['username', 'nick_name', 'first_name', 'last_name', 'email', 'gender', 'address', 'mobile']
#     search_fields = ['username', 'nick_name']
#     list_filter = ['username', 'nick_name', 'first_name', 'last_name', 'email', 'gender', 'address', 'mobile']


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    '''
    下面的model_icon功能是实现在EmailVerifyRecordAdmin里面的表格加上自定义的图标
    '''
    model_icon = 'fa fa-car'

class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']

# xadmin.site.unregister(User)
# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)