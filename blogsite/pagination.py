from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from blogsite.models import Comment


class BlogPagination(PageNumberPagination):
    """ 自定义博客分页类 """

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('blog_count', self.page.paginator.count),
            ('comment_count', Comment.objects.filter(is_valid=True).count()),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))
