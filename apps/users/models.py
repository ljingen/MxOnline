# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class UserProfile(AbstractUser):
    # 性别选择器
    SEX_IN_USER_CHOICES = (
        ('MALE', u'男'),
        ('FEMALE', u'女'),
    )
    nick_name = models.CharField(
        max_length=50,
        verbose_name=u'昵称',
        default=u'')
    birthday = models.DateField(verbose_name=u'生日', default=timezone.now)
    gender = models.CharField(
        max_length=6,
        verbose_name=u'性别',
        choices=SEX_IN_USER_CHOICES,
        default='MALE')
    address = models.CharField(max_length=100, verbose_name=u'地址', default=u'')
    mobile = models.CharField(max_length=11, verbose_name='手机号', null=True, blank=True)
    image = models.ImageField(max_length=100, upload_to='image/%Y/%M/%D', default=u'image/default.png',verbose_name=u'用户头像')
    sign = models.CharField(max_length=100, verbose_name='个性签名', null=True, blank=True,default=u'这家伙很懒,什么都没留下')
    classroom = models.CharField(max_length=2, verbose_name='班级', null=True, blank=True)

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(choices=(('register', u'注册'), ('course_orgcourse_orgcourse_orgcourse_orgcourse_orgcourse_orgcourse_orgcourse_orgcourse_orgcourse_org', u'找回密码')), max_length=10, verbose_name='验证码类型')
    send_time = models.DateTimeField(default=timezone.now, verbose_name=u'发送时间')

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    title = models.CharField(max_length=50, verbose_name=u'标题')
    image = models.ImageField(upload_to='image/%Y/%M/%D', verbose_name=u'轮播图', max_length=100)
    url = models.URLField(max_length=100, verbose_name=u'访问地址')
    index = models.IntegerField(default=100, verbose_name=u'顺序')
    add_time= models.DateTimeField(default=timezone.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name