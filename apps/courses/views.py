# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 引入分页器

from operation.models import UserFavorite, CourseComments
from .models import Course, CourseResource
# Create your views here.


class CourseListView(View):
    """
    获取课程列表
    """
    def get(self, request):
        """从数据库获取所有课程"""
        all_course = Course.objects.all().order_by('-add_time')
        hot_course = Course.objects.all().order_by('-click_num')[:3]
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


class CourseInfoView(View):
    """
    课程的章节信息
    """
    def get(self, request, course_id):
        """从数据库获取所有课程"""
        course = Course.objects.get(id=int(course_id))

        all_lessons = course.lesson_set.all()

        all_resource = CourseResource.objects.filter(course=course)

        return render(request, 'course-video.html', {
            'course': course,  # 根据course_id返回course实例
            'all_lessons': all_lessons,  # 返回当前课程所属的所有章节
            'course_resources': all_resource
        })


class CommentsView(View):
    """
    课程评论相关内容
    """
    def get(self, request, course_id):
        """从数据库获取所有课程"""
        course = Course.objects.get(id=int(course_id))

        all_lessons = course.lesson_set.all()

        all_resource = CourseResource.objects.filter(course=course)

        all_comments = CourseComments.objects.all()

        return render(request, 'course-comment.html', {
            'course': course,  # 根据course_id返回course实例
            'all_lessons': all_lessons,  # 返回当前课程所属的所有章节
            'course_resources': all_resource,  # 返回当前课程的所有资源
            'all_comments': all_comments  # 返回所有的评论列表
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
