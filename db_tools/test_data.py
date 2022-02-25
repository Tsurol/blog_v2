import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_v2.settings")

import django

django.setup()

import random
from blogsite.models import Blog, Category, Comment, LoveRelated
from authentication.models import AuthUser

""" 导入测试数据 """

# Category.objects.create(name='学习笔记')
# Category.objects.create(name='技术博客')
# Category.objects.create(name='转载文档')

category1 = Category.objects.filter(name='学习笔记').first()
category2 = Category.objects.filter(name='技术博客').first()
category3 = Category.objects.filter(name='转载文档').first()
user_test = AuthUser.objects.get(id=3)
random_cat = [category3, category2, category1]

# for i in range(1, 26):
#     Blog.objects.create(title='测试标题{}'.format(i), desc='测试简述{}'.format(i),
#                         content='测试正文{}'.format(i), category=random.choice(random_cat), user=user_test)

blog1 = Blog.objects.get(id=3)
blog2 = Blog.objects.get(id=4)
blog3 = Blog.objects.get(id=5)
random_blog = [blog1, blog2, blog3]
# for i in range(10):
#     Comment.objects.create(content='测试评论{}'.format(i), user=user_test, blog=random.choice(random_blog))

comment1 = Comment.objects.get(id=1)
comment2 = Comment.objects.get(id=2)
comment3 = Comment.objects.get(id=3)
random_comment = [comment1, comment2, comment3]

for i in range(10):
    blog_love = LoveRelated(content_object=random.choice(random_blog), user=user_test)
    blog_love.save()

for i in range(5):
    comment_love = LoveRelated(content_object=random.choice(random_comment), user=user_test)
    comment_love.save()
