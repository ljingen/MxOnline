# -*- coding: utf-8 -*-
from django import forms

from operation.models import UserAsk


class UserAskFrom(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['user', 'mobile', 'course_name']