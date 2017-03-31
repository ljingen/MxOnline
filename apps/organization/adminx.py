# -*- coding: utf-8 -*-
import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['city', 'name', 'desc', 'address', 'fav_nums', 'click_num', 'add_time']
    search_fields = ['city', 'name', 'desc', 'address', 'fav_nums', 'click_num']
    list_filter = ['city', 'name', 'desc', 'address', 'fav_nums', 'click_num', 'add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'desc', 'work_years', 'work_company', 'add_time']
    search_fields = ['org', 'name', 'desc', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'desc', 'work_years', 'work_company', 'add_time']

xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CityDict, CityDictAdmin)

