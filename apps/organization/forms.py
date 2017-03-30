# -*- coding: utf-8 -*-
import re

from django import forms

from operation.models import UserAsk


class UserAskFrom(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['user', 'mobile', 'course_name']

    def clean_mobile(self):
        ''''
        验证手机号码是否合法,
        自定义的数据验证，必须以clean开头的方法，另外在调用数据采用sele.cleaned_data['arg']形式
        :return: 
        '''
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码非法', code='mobile_invalid')
