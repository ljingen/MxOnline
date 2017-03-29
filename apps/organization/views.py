# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 引入分页器
from .models import CityDict, CourseOrg
# Create your views here.


class OrgListView(View):

    def get(self, request):
        all_city = CityDict.objects.all()
        all_courseorg = CourseOrg.objects.all()
        courseorg_num = all_courseorg.count()

        city_id = request.GET.get('city', "")
        if city_id:
            all_courseorg = all_courseorg.filter(city_id=int(city_id))

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = 1
        paginator = Paginator(all_courseorg, 5, request=request)  # 获取一共有多少个页面
        all_orgs = paginator.page(page)  # 拿到指定的分页




        return render(request, 'org-list.html', {
            'all_orgs': all_orgs,  # 分页选择器
            'all_city': all_city,
            'courseorg_num': courseorg_num,
            'city_id': city_id,
        })

    def post(self, request):
        pass