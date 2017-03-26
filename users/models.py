# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils import timezone


class UserProfile(AbstractUser):
    # 性别选择器
    SEX_IN_USER_CHOICES = (
        ('MAN', u'男'),
        ('FEMALE', u'女'),
    )
    nick_name = models.CharField(
        max_length=50,
        verbose_name=u'昵称',
        default=u'')
    birthday = models.DateField(verbose_name=u'生日', default=timezone.now)
    gender = models.CharField(
        max_length=5,
        verbose_name=u'性别',
        choices=SEX_IN_USER_CHOICES,
        default='MAN')
    address = models.CharField(max_length=100, verbose_name=u'地址', default=u'')
    mobile = models.CharField(max_length=11, verbose_name='手机号', null=True, blank=True)
    image = models.ImageField(max_length=100, upload_to='image/%Y/%M/%D', default=u'image/default.png')
    sign = models.CharField(max_length=100, verbose_name='个性签名', null=True, blank=True,default=u'这家伙很懒,什么都没留下')
    classroom = models.CharField(max_length=2, verbose_name='班级', null=True, blank=True)
    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


