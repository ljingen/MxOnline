# -*- coding: utf-8 -*-
import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse


class LessionInline(object):
    model = Lesson
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'add_time']
    search_fields = ['name', 'degree']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'add_time']
    ordering = ['-click_num']
    readonly_fields = ['click_num', 'fav_nums']
    style_fields = {'detail':'ueditor'}
    inlines = [LessionInline]


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'add_time']
    search_fields = ['name', 'degree']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'add_time']
    ordering = ['-click_num']
    readonly_fields = ['click_num', 'fav_nums']

    inlines = [LessionInline]
    '''
    对父Course进行过滤，找到是banner的表
    '''
    def queryset(self):
        qs = super(BannerCourseAdmin,self).queryset()
        qs = qs.filter(is_banner=True)
        return qs

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course__name', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    pass


class CourseResourceAdmin(object):
    pass

xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
