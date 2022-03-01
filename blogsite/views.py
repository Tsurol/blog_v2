from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from blogsite.filters import BlogFilter
from blogsite.models import Blog, Tag, Comment
from blogsite.pagination import BlogPagination
from blogsite.serializers import BlogSerializer, TagSerializer, CommentSerializer
from rest_framework import filters


class BlogViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ 博客列表接口 """
    queryset = Blog.objects.filter(is_valid=True)
    pagination_class = BlogPagination
    serializer_class = BlogSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('title', 'desc')  # 不区分大小写的部分匹配
    filter_class = BlogFilter
    # filter_fields = ('is_hot', 'is_top')  # 精确过滤=
    ordering_fields = ['is_top', 'created_at']


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ 标签列表接口 """
    queryset = Tag.objects.filter(is_valid=True)
    pagination_class = None
    serializer_class = TagSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('blog',)


class CommentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ 评论列表接口 """
    queryset = Comment.objects.filter(is_valid=True).order_by('-created_at')
    pagination_class = PageNumberPagination
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  # todo 测试jwt
