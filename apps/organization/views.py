# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 引入分页器
from .models import CityDict, CourseOrg, Teacher
from courses.models import Course
from django.db.models import Q
from .forms import UserAskFrom
from operation.models import UserFavorite
# Create your views here.


class OrgListView(View):

    def get(self, request):
        all_city = CityDict.objects.all()
        all_courseorg = CourseOrg.objects.all()

        '''取出热门城市列表，利用django的筛选功能'''
        hot_courseorg = all_courseorg.order_by('-click_num')[:5]
        '''根据关键字进行搜索'''
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_courseorg = all_courseorg.filter(Q(name__icontains=search_keywords) |
                                                 Q(desc__icontains=search_keywords) |
                                                 Q(detail__icontains=search_keywords))
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
            'all_orgs': all_orgs,  # 分页选择器，传过去之后需要有一个变量 object_list获取里面的对象
            'all_city': all_city,
            'courseorg_num': courseorg_num,
            'city_id': city_id,
            'category': category,
            'hot_courseorg': hot_courseorg,
            'sort': sort,
        })

    def post(self, request):
        pass


class AddUserAskView(View):
    def get(self, request):
        return ('hello')

    def post(self, request):
        # create a form instance and populate it with data from the request:
        userask_form = UserAskFrom(request.POST)
        # check whether it's valid:
        if userask_form.is_valid():
            # Create, and save the new userask instance.
            new_ask = userask_form.save(commit=True)

            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse('{"status": "fail","msg":"添加出错了","name":"金刚狼"}', content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'  # 用作判断当前是访问哪个页面

        course_org = CourseOrg.objects.get(id=int(org_id))
        all_course = course_org.course_set.all()[:3]
        all_teacher = Teacher.objects.filter(org=int(org_id))[:1]
        # 判读用户是否已经收藏了
        hav_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
            hav_fav = True

        return render(request, 'org-detail-homepage.html', {
            'all_course': all_course,  # 当前机构的所有课程
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,  #返回当前页是哪页，控制csss active2状态
            'hav_fav': hav_fav  # 返回收藏结构
         })


class OrgCourseView(View):
    """
    机构课程列表页面
    """
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_course = course_org.course_set.all()
        # 判读用户是否已经收藏了
        hav_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
            hav_fav = True

        return render(request, 'org-detail-course.html', {
            'all_course': all_course,  # 当前机构的所有课程
            'course_org': course_org,
            'current_page': current_page,  #返回当前页是哪页，控制csss active2状态
            'hav_fav': hav_fav  # 返回收藏结构
         })


class OrgDescView(View):
    """
    机构详情介绍页面
    """
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_course = course_org.course_set.all()
        # 判读用户是否已经收藏了
        hav_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
            hav_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,  # 返回机构对象
            'current_page': current_page,  # 返回当前页是哪页，控制csss active2状态
            'hav_fav': hav_fav  # 返回收藏结构
         })


class OrgTeacherView(View):
    """
    机构教师页面
    """
    def get(self, request, org_id):
        current_page = 'teacher'  # 如果当前页面是教师，那么让教师的list含有active2
        course_org = CourseOrg.objects.get(id=int(org_id))
        """
        这个地方需要重点关注，这个是 CoureseOrg是一个model, Teacher这个model有个外键指向了CourseOrg
        所以这个地方可以使用teacher_set来从CourseOrg访问所有他的老师
        在教师列表中访问所有 机构id为1的教师可以用
        all_teacher = Teacher.filter(courseorg_id = int(course_id))
        已知老师，查他的所属机构，可以用
        teacher.couseorg_id.name；直接访问就可以
        
        all_courseorg =CourserOrg.object.all()
        city_id = request.GET.get('city', '')
        if city_id:
            all_courseorg = all_courseorg.filter(city_id=int(city_id))
        """
        all_teacher = course_org.teacher_set.all()
        # 判读用户是否已经收藏了
        hav_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                hav_fav = True

        return render(request, 'org-detail-teachers.html', {
            'all_teacher': all_teacher,  # 当前机构的所有教师
            'course_org': course_org,
            'current_page': current_page,  # 返回当前页是哪页，控制csss active2状态
            'hav_fav': hav_fav  # 返回收藏结构
         })


class AddFavView(View):
    """
    收藏的功能，取消收藏功能
    """
    def get(self,request):
        return render(request , 'send_success.html', {})

    def post(self,request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        user = request.user
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail","msg":"用户未登录","name":"金刚狼"}', content_type='application/json')
        exist = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist:
            if int(fav_id) > 0 and int(fav_type) > 0:
                exist.delete()
                return HttpResponse('{"status": "success","msg":"收藏","name":"金刚狼"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail","msg":"添加错了","name":"金刚狼"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            user_fav.user = request.user
            user_fav.fav_id = int(fav_id)
            user_fav.fav_type = int(fav_type)
            user_fav.save()
            return HttpResponse('{"status": "success","msg":"已收藏","name":"金刚狼"}', content_type='application/json')


class TeacherListView(View):

    def get(self, request):

        all_teachers = Teacher.objects.all()

        hot_teachers = Teacher.objects.all().order_by('-click_num')[:5]
        '''根据关键字进行搜索'''
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                                 Q(desc__icontains=search_keywords) |
                                                 Q(points__icontains=search_keywords))

        '''按照类别进行排序'''
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_num')
        '''处理页面分页'''
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = 1
        paginator = Paginator(all_teachers, 10, request=request)  # 获取一共有多少个页面
        all_teachers = paginator.page(page)  # 拿到指定的分页

        return render(request, 'teachers-list.html', {
            'all_teachers': all_teachers,  # 获取所有的教师列表，返回给前端处理
            'sort': sort,  # 返回按照热度进行排序
            'hot_teachers': hot_teachers,  # 返回当前热门的教师列表，按照点击数进行排行，返回5个
        })


class TeacherDetailView(View):

    def get(self, request, teacher_id):

        current_page = 'teacher'  # 用作判断当前是访问哪个页面

        teacher = Teacher.objects.get(id=int(teacher_id))

        hot_teachers = Teacher.objects.all().order_by('-click_num')[:5]

        # 方法1，因为ourse有一个外键指向Teacher表，所以可以用teacher.course_set来找到当前教师所有课程
        teacher_courses = teacher.course_set.all();

        #  方法2,因为course里面有一个teacher字段，所以可以直接从course表里面查询所有教师是teacher的课程
        teacher_courses = Course.objects.filter(teacher=teacher)

        #  判断用户是否已经收藏
        has_fav_teacher = False
        has_fav_organization = False
        if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
            has_fav_teacher = True
        if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
            has_fav_organization = True

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,  # 根据传进来的教师id，获取教师信息
            'teacher_courses': teacher_courses,  # 返回当前教师的所有课程信息
            'hot_teachers': hot_teachers,  # 返回当前热门教师
            'has_fav_teacher': has_fav_teacher,  # 返回收藏教师信息
            'has_fav_organization': has_fav_organization,  # 返回收藏机构信息

        })
