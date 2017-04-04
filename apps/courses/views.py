# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 引入分页器
from django.db.models import Q

from operation.models import UserFavorite, CourseComments, UserCourse
from .models import Course, CourseResource
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    """
    获取课程列表
    """
    def get(self, request):
        """从数据库获取所有课程"""
        all_course = Course.objects.all().order_by('-add_time')
        hot_course = Course.objects.all().order_by('-click_num')[:3]
        '''根据关键字进行搜索'''
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_course = all_course.filter(Q(name__icontains=search_keywords) |
                                           Q(desc__icontains=search_keywords) |
                                           Q(detail__icontains=search_keywords))
        '''按照类别进行排序'''
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_course = all_course.order_by('-students')
            elif sort == 'hot':
                all_course = all_course.order_by('-click_num')
        '''处理页面分页'''
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = 1
        paginator = Paginator(all_course, 10, request=request)  # 获取一共有多少个页面
        all_course_page = paginator.page(page)  # 拿到指定的分页

        return render(request, 'course-list.html', {
            'all_course_page': all_course_page,  # 分页选择器，传过去之后需要有一个变量 object_list获取里面的对象
            'sort': sort,  # 用来控制html里面那个标签当前应该显示
            'hot_course': hot_course  # 返回给前端3个热门的课程
        })

    def post(self, request):
        pass


class CourseDetailView(View):
    """
    获取课程详情信息
    """
    def get(self, request, course_id):
        """从数据库获取所有课程"""
        course = Course.objects.get(id=int(course_id))
        #  增加课程点击数
        course.click_num += 1
        course.save()
        #根据tag来进行对应的可能还喜欢
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag =tag)[:1]
        else:
            relate_courses = []
        #返回用户是否收藏的逻辑
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.org.id, fav_type=2):
                has_fav_org = True

        return render(request, 'course-detail.html', {
            'course': course,  # 根据course_id返回course实例
            'relate_courses': relate_courses,  # 根据tag，在整个couse里面查找相同tag的couse
            'has_fav_course': has_fav_course,  # 返回用户是否收藏了该课程
            'has_fav_org': has_fav_org  # 返回用户是否收藏了该机构
        })

    def post(self, request):
        pass


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程的章节信息
    """
    def get(self, request, course_id):
        """从数据库获取所有课程"""
        course = Course.objects.get(id=int(course_id))
        """用户点击课程后，查看用户是否已经学习过该课程"""
        user_courses = UserCourse.objects.filter(course=course)
        if not user_courses:
            user_course = UserCourse(user = request.user, course=course)
            user_course.save()
        """看过这门课程的同学还看过什么课程"""
        user_courses = UserCourse.objects.filter(course=course)
        # 把看过这门课程的所有用户的id都取出来
        user_ids = [user_course.user.id for user_course in user_courses]
        # 根据这些User_ids，我们把所有这些用户学过的课程用户表都取出来
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 我们再把这些课程用户表里面的course_id给取出来
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 根据所有的这些课程id，我们从Course表里面，再把所有的Course取出来
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]

        all_lessons = course.lesson_set.all()

        all_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-video.html', {
            'course': course,  # 根据course_id返回course实例
            'all_lessons': all_lessons,  # 返回当前课程所属的所有章节
            'course_resources': all_resources,  # 返回当前课程关联的资源清单
            'relate_courses': relate_courses,  # 返回所有学过这门课还学过的课的信息
        })


class CourseCommentsView(LoginRequiredMixin, View):
    """
    课程评论相关内容
    """
    def get(self, request, course_id):
        """从数据库获取所有课程"""
        course = Course.objects.get(id=int(course_id))
        """用户点击课程后，查看用户是否已经学习过该课程"""
        user_courses = UserCourse.objects.filter(course=course)
        if not user_courses:
            user_course = UserCourse(user = request.user, course=course)
            user_course.save()
        """看过这门课程的同学还看过什么课程"""
        user_courses = UserCourse.objects.filter(course=course)
        # 把看过这门课程的所有用户的id都取出来
        user_ids =[user_course.user.id for user_course in user_courses]
        # 根据这些User_ids，我们把所有这些用户学过的课程用户表都取出来
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 我们再把这些课程用户表里面的course_id给取出来
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 根据所有的这些课程id，我们从Course表里面，再把所有的Course取出来
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]

        all_lessons = course.lesson_set.all()

        all_resource = CourseResource.objects.filter(course=course)

        all_comments = CourseComments.objects.all().order_by('-add_time')

        return render(request, 'course-comment.html', {
            'course': course,  # 根据course_id返回course实例
            'all_lessons': all_lessons,  # 返回当前课程所属的所有章节
            'course_resources': all_resource,  # 返回当前课程的所有资源
            'all_comments': all_comments,  # 返回所有的评论列表
            'relate_courses': relate_courses,  # 返回所有学过这门课还学过的课的信息
        })


class AddCommentsView(View):
    """
    从ajax发起添加课程的评论
    """
    def post(self, request):

        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail","msg":"用户未登录","name":"金刚狼"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        """从数据库获取Course实例"""
        course = Course.objects.get(id=int(course_id))

        if course_id > 0 and comments:
            course_comment = CourseComments()
            course_comment.user = request.user
            course_comment.course = course
            course_comment.comments = comments
            course_comment.save()
            return HttpResponse('{"status": "success","msg":"添加成功","name":"金刚狼"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail","msg":"添加失败","name":"金刚狼"}', content_type='application/json')
