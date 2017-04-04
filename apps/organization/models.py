# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.utils import timezone
from django.db import models

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'城市名', default=u'')
    desc = models.CharField(max_length=200, verbose_name=u'城市描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):

    city = models.ForeignKey(CityDict,verbose_name=u'所属城市')
    name = models.CharField(max_length=50, verbose_name=u'机构名称', default=u'')
    desc = models.CharField(max_length=300, verbose_name=u'机构描述')
    address = models.CharField(max_length=100, verbose_name=u'机构地址')
    image = models.ImageField(upload_to='organization/%Y/%M/%D', verbose_name=u'封面图', default='organization/default.png')
    detail = models.TextField(verbose_name=u'机构介绍')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')

    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_nums = models.IntegerField(default=0, verbose_name=u'课程数')

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    category = models.CharField(max_length=10,
                                choices=(('pxjg', u'培训机构'), ('gr', u'个人讲师'), ('gx', u'高等院校')),
                                default='pxjg',
                                verbose_name='类别')

    class Meta:
        verbose_name = u'机构'
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        """返回当前机构所含的教师数量"""
        return self.teacher_set.all().count()

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构')
    name = models.CharField(max_length=50, verbose_name=u'教师名称', default=u'')
    desc = models.CharField(max_length=300, verbose_name=u'教师描述')
    work_years = models.CharField(max_length=10, verbose_name= u'工作年限')
    work_company = models.CharField(max_length=10, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=10, verbose_name=u'就职职位')
    age = models.IntegerField(default=0, verbose_name=u'年龄')
    image = models.ImageField(upload_to='organization/%Y/%M/%D', verbose_name=u'头像', default='organization/default.png')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    points = models.CharField(max_length=50, verbose_name=u'教学特点')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name