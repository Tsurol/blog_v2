import random

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .models import Blog, Tag
from django_filters import rest_framework as filters


class BlogFilter(filters.FilterSet):
    """ 自定义博客的过滤类 """
    is_hot = filters.BooleanFilter(field_name='is_hot', lookup_expr='exact')
    is_top = filters.BooleanFilter(field_name='is_top', lookup_expr='exact')
    tag_id = filters.NumberFilter(method='tag_filter')
    related_id = filters.NumberFilter(method='related_filter')

    def tag_filter(self, queryset, name, value):
        """ 根据标签过滤查询出博客 """
        tag_qs = Tag.objects.filter(id=value)
        if tag_qs:
            tag_qs = tag_qs[0]
            queryset = tag_qs.blog.filter(is_valid=True).all()
            return queryset

    def related_filter(self, queryset, name, value):
        """ 根据标题或简述过滤查询出博客 """
        blog_qs = Blog.objects.filter(id=value, is_valid=True).first()
        if blog_qs.keyword:
            queryset = queryset.filter(
                Q(is_valid=True, title__icontains=blog_qs.keyword) | Q(is_valid=True, desc__icontains=blog_qs.keyword)) \
                .exclude(id=value)
            if queryset.count() >= 5:
                queryset = queryset[:5]
            elif queryset.count() == 0:
                queryset = Blog.objects.filter(is_valid=True).order_by('-created_at')[:5]
        else:
            queryset = Blog.objects.filter(is_valid=True).order_by('-created_at')[:5]

        return queryset

    class Meta:
        model = Blog
        fields = ['is_hot', 'is_top', 'tag_id', 'related_id']
