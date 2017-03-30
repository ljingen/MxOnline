# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 引入分页器
from .models import CityDict, CourseOrg
from .forms import UserAskFrom
# Create your views here.


class OrgListView(View):

    def get(self, request):
        all_city = CityDict.objects.all()
        all_courseorg = CourseOrg.objects.all()

        '''取出热门城市列表，利用django的筛选功能'''
        hot_courseorg = all_courseorg.order_by('-click_num')[:5]

        '''城市筛选功能'''
        city_id = request.GET.get('city', '')
        if city_id:
            all_courseorg = all_courseorg.filter(city_id=int(city_id))
        '''机构类别筛选'''
        category = request.GET.get('ct', '')
        if category:
            all_courseorg = all_courseorg.filter(category=category)
        '''按照类别进行排序'''
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courseorg = all_courseorg.order_by('-students')
            elif sort == 'course':
                all_courseorg = all_courseorg.order_by('-course_nums')

        '''符合条件的机构数量'''
        courseorg_num = all_courseorg.count()
        '''处理页面分页'''
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
            'category': category,
            'hot_courseorg': hot_courseorg,
            'sort': sort,
        })

    def post(self, request):
        pass


class UserAskView(View):
    def post(self, request):
        # create a form instance and populate it with data from the request:
        userask_form = UserAskFrom(request.POST)
        # check whether it's valid:
        if userask_form.is_valid():
            # Create, and save the new userask instance.
            new_ask = userask_form.save(commit=True)