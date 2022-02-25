import random

from faker import Faker

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models, transaction
from .spider import CrawlProject


class AuthUserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given steamid and password.
        """
        with transaction.atomic():
            user = self.model(**extra_fields)
            user.set_password(password)
            user.username = username
            user.save(using=self._db)
            profile = UserProfile.objects.create(user=user, username=username)
            profile.nickname = profile.create_random_nickname
            profile.save()
            UserAsset.objects.create(user=user, coins=10, username=user.username)
            LoginRecord.objects.create(user=user, username=user.username)
        return user

    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class AuthUser(AbstractUser):
    mobile = models.CharField('手机号', max_length=11, null=True, blank=True)
    name = models.CharField('姓名', max_length=5, null=True, blank=True)
    objects = AuthUserManager()

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
        db_table = 'auth_user'

    def __str__(self):
        return self.username

    def update_coins(self, amount, remark=None):
        """ 更新账户鲨币 """
        with transaction.atomic():
            if amount == 0:
                return
            # select_for_update来告诉数据库锁定对象，直到事务完成
            asset = UserAsset.objects.select_for_update().get(user=self)
            if asset.coins + amount < 0:
                raise Exception('鲨币余额不足')
            coins_before = asset.coins
            asset.coins += amount
            asset.save()
            coins_after = asset.coins
            UserCoinsRecord.objects.create(
                user=self, coins_changed=amount, coins_before=coins_before,
                coins_after=coins_after, reason=remark)


class UserProfile(models.Model):
    MAN = 0
    WOMAN = 1
    SEX_CHOICES = [
        (0, 'male'),
        (1, 'female'),
    ]
    username = models.CharField('用户名(手机号)', max_length=11, editable=False, default=None, help_text='冗余字段')
    nickname = models.CharField('昵称', max_length=8, default=None, null=True, blank=True)
    avatar = models.ImageField('头像地址', max_length=120, null=True, blank=True, upload_to='auth/avatar/',
                               default='avatar/default_avatar.jpg')
    sex = models.CharField('性别', max_length=1, choices=SEX_CHOICES, default=MAN)
    birthday = models.DateTimeField('出生年月', null=True, blank=True)
    words = models.CharField('个性签名', max_length=15, null=True, blank=True, default='他很懒，什么也没留下')
    is_valid = models.BooleanField('逻辑删除', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)
    user = models.OneToOneField(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE, related_name='profile')

    class Meta:
        verbose_name = '用户详细信息'
        verbose_name_plural = '用户详细信息'
        db_table = 'auth_user_profile'

    def __str__(self):
        return self.avatar

    @property
    def create_random_nickname(self):
        """
        用户注册时，为用户创建随机的个性昵称
        :return:
        """
        headers = {
            'User-Agent': Faker().user_agent()
        }
        try:
            crawl = CrawlProject(url='https://www.qunzou.com/wangming/11052.html', headers=headers)
            random_nickname = random.choice(crawl.nickname_ls)
        except Exception as e:
            print(e)
            return '{}{}号'.format('小可爱', self.id)
        # todo nickname可能会重复
        return '{}'.format(random_nickname)


class LoginRecord(models.Model):
    username = models.CharField('用户名(手机号)', max_length=11, editable=False, default=None, help_text='冗余字段')
    ip = models.CharField('IP地址', max_length=50, null=True, blank=True)
    source = models.CharField('登录来源', max_length=30, null=True, blank=True, default='web')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    user = models.ForeignKey(verbose_name='关联用户', to=AuthUser,
                             on_delete=models.CASCADE, related_name='login_record')

    class Meta:
        db_table = 'auth_login_record'
        verbose_name = '登录历史'
        verbose_name_plural = '登录历史'

    def __str__(self):
        return self.ip


class UserAsset(models.Model):
    username = models.CharField('用户名(手机号)', max_length=11, editable=False, default=None, help_text='冗余字段')
    coins = models.FloatField("账户鲨币", default=0.0)
    updated_at = models.DateTimeField('修改时间', auto_now=True)
    user = models.OneToOneField(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE, related_name='asset')
    is_valid = models.BooleanField('逻辑删除', default=True)

    class Meta:
        db_table = 'auth_user_asset'
        verbose_name = '用户资产'
        verbose_name_plural = '用户资产'

    def __str__(self):
        return self.username


class UserCoinsRecord(models.Model):
    username = models.CharField('用户名', max_length=150, editable=False, default=None)
    coins_changed = models.IntegerField("鲨币变化数量", default=0)
    coins_before = models.IntegerField("鲨币变化前数量", default=0)
    coins = models.IntegerField("当前鲨币数量", default=0)
    reason = models.CharField("备注信息", max_length=256, default=None, null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)
    user = models.ForeignKey(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE, related_name='coins_record')

    class Meta:
        db_table = 'auth_user_coins_record'
        verbose_name = '交易记录'
        verbose_name_plural = '交易记录'

    def __str__(self):
        return self.coins
