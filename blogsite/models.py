from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from mdeditor.fields import MDTextField
from datetime import datetime
import timeago
from authentication.models import AuthUser


class CommonModel(models.Model):
    is_valid = models.BooleanField('逻辑删除', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True


class Blog(CommonModel):
    title = models.CharField('标题', max_length=30)
    desc = models.CharField('简述', max_length=120)
    content = MDTextField()
    is_top = models.BooleanField('置顶', default=False)
    is_hot = models.BooleanField('热门博客', default=False)
    # bkc = models.CharField('背景颜色', max_length=32, null=True, default='#adb5bd', blank=True)
    # img = models.CharField('图片地址', max_length=256, null=True, blank=True, default=None)
    img = models.ImageField('图片地址', max_length=300, null=True, blank=True, upload_to='blog/cover/', default=None)
    is_origin = models.BooleanField('是否原创', default=True)
    # todo：keyword为必填字段
    keyword = models.CharField('关键词', null=True, blank=True, max_length=16)
    user = models.ForeignKey(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE,
                             related_name='blog_list')
    love = GenericRelation(to='LoveRelated', verbose_name='关联点赞表')
    category = models.ForeignKey(verbose_name='关联分类专栏', to='Category', on_delete=models.SET_NULL, null=True,
                                 related_name='category_blog_list')

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = '博客'
        db_table = 'blog_blog'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def cat_name(self):
        return self.category.name

    @property
    def author(self):
        return self.user.profile.nickname

    @property
    def format_created_at(self):
        return self.created_at.strftime('%Y-%m-%d')

    @property
    def comment_count(self):
        return self.blog_comment_list.filter(is_valid=True).count()

    @property
    def love_count(self):
        return self.love.filter(is_valid=True).count()


class Comment(CommonModel):
    content = models.TextField('评论内容')
    is_top = models.BooleanField('置顶', default=False)
    reply = models.ForeignKey(verbose_name='评论的回复', to='self', blank=True, null=True,
                              related_name='comment_reply',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE,
                             related_name='user_comment_list', null=True, blank=True)
    blog = models.ForeignKey(verbose_name='关联博客', to=Blog, on_delete=models.CASCADE,
                             related_name='blog_comment_list')
    love = GenericRelation(to='LoveRelated', verbose_name='关联点赞表')

    @property
    def format_created_at(self):
        now = datetime.now()
        return timeago.format(self.created_at, now, 'zh_CN')

    @property
    def author(self):
        return self.user.profile.nickname

    @property
    def blog_title(self):
        return self.blog.title

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        db_table = 'blog_comment'

    def __str__(self):
        return self.content


class Tag(CommonModel):
    name = models.CharField('标签名称', max_length=12)
    bkc = models.CharField('背景色', max_length=12, default='#7fd5ea')
    blog = models.ManyToManyField(verbose_name='关联博客', to=Blog,
                                  related_name='blog_tag_list')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        db_table = 'blog_Tag'

    def __str__(self):
        return self.name


class LoveRelated(models.Model):
    user = models.ForeignKey(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE,
                             related_name='user_love_list')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='关联的模型')
    object_id = models.PositiveIntegerField('具体对象id')
    content_object = GenericForeignKey('content_type', 'object_id')

    is_valid = models.BooleanField('逻辑删除', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = '点赞'
        db_table = 'Love_related'

    def __str__(self):
        return self.id


class AdviceUpload(models.Model):
    """ 需求提交 """
    name = models.CharField('姓名', max_length=12)
    mobile = models.CharField('联系方式', max_length=11)
    advice = models.CharField('建议', max_length=256)
    remarks = models.CharField("备注信息", max_length=256, null=True, blank=True, default=None)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = '反馈建议'
        verbose_name_plural = '反馈建议'
        db_table = 'blog_advice'

    def __str__(self):
        return self.id


class Category(models.Model):
    """ 分类专栏 """
    name = models.CharField('专栏名', max_length=64)
    remarks = models.CharField("备注信息", max_length=256, null=True, blank=True, default=None)
    create_time = models.DateTimeField("创建时间", auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = '分类专栏'
        verbose_name_plural = '分类专栏'
        db_table = 'blog_category'

    def __str__(self):
        return self.name
