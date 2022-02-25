from rest_framework import serializers

from blogsite.models import Blog, Tag, Comment


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'format_created_at', 'author', 'img',
                  'title', 'desc', 'is_top', 'is_hot', 'comment_count',
                  'love_count', 'keyword', 'is_origin', 'cat_name', 'content')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'bkc', 'blog')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'blog_title', 'content', 'format_created_at')
