# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from .views import OrgListView

urlpatterns = [
    url(r'^list/$', OrgListView.as_view(), name='orglist'),
    url(r'user_ask/$',UserAskView)
]