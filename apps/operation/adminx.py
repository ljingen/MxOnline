# -*- coding: utf-8 -*-
import xadmin

from .models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse


class UserAskAdmin(object):
    pass
xadmin.site.register(UserAsk, UserAskAdmin)


class CourseCommentsAdmin(object):
    pass
xadmin.site.register(CourseComments, CourseCommentsAdmin)


class UserFavoriteAdmin(object):
    pass
xadmin.site.register(UserFavorite, UserFavoriteAdmin)


class UserMessageAdmin(object):
    pass
xadmin.site.register(UserMessage, UserMessageAdmin)


class UserCourseAdmin(object):
    pass
xadmin.site.register(UserCourse, UserCourseAdmin)