# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import DjangoUeditor

from django.utils import timezone
from django.db import models

from DjangoUeditor.models import UEditorField
from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构', null=True, blank=True, default='')
    teacher = models.ForeignKey(Teacher, verbose_name=u'任课教师', null=True, blank=True, default='')
    name = models.CharField(max_length=50, verbose_name=u'课程名', default=u'')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = UEditorField(verbose_name=u'课程详情	',
                          width=600,
                          height=300,
                          toolbars="normal",
                          imagePath="course/ueditor/",
                          filePath="course/ueditor/",
                          upload_settings={"imageMaxSize": 1204000},
                          settings={},
                          command=None,
                          blank=True,
                          default='')
    is_banner = models.BooleanField(default=False, verbose_name= u'是否轮播')
    degree = models.CharField(max_length=5, choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级'),), verbose_name=u'难度')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%M/%D', verbose_name=u'logo', default='courses/default.png')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    category = models.CharField(max_length=20, verbose_name=u'课程类别', default='')
    tag = models.CharField(max_length=20, verbose_name=u'课程标签', default='')
    tips_needs = models.TextField(verbose_name=u'老师告诉你能学到什么', default='')
    course_notes = models.TextField(verbose_name=u'课程须知', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_learn_users(self):
        #  获取学习用户
        return self.usercourse_set.all()[:5]

    def get_zj_nums(self):
        #  获取章节数
        all_lessons = self.lesson_set.all().count()
        return all_lessons

    def get_course_lesson(self):
        #  获取课程所有章节
        return self.lesson_set.all()

    def get_course_comments(self):
        # 获取章节的所有评论，因为评论是课程的子表，在评论有章节的外键，所以可以用下面方法
        return self.coursecomments_set.all()

    def __unicode__(self):
        return self.name

'''
继承自Course，管理轮播图课程
关键知识点是  proxy必须设置
'''
class BannerCourse(Course):
    class Meta:
        verbose_name = u'课程轮播图'
        verbose_name_plural = verbose_name
        proxy = True

class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_video(self):
        #  获取课程所有章节
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url = models.CharField(max_length=200, verbose_name=u'访问地址', default='')
    learn_times = models.IntegerField(default=0, verbose_name=u'视频时长')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=50, verbose_name=u'名称')
    download = models.FileField(upload_to='course/%Y/%M/%D', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
