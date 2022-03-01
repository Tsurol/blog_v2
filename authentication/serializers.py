import ast
import re
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from authentication.utils import decode_base64

User = get_user_model()


class EmailCodeSerializer(serializers.Serializer):
    """ 发送邮箱验证码 """
    # 为啥不用ModelSerializer，因为发送验证码只需要email字段
    email = serializers.CharField(required=True, allow_blank=False, max_length=32,
                                  label='邮箱', error_messages={'blank': '邮箱不能为空',
                                                              'required': '请输入邮箱',
                                                              'max_length': '邮箱长度不得超过32'})

    def validate_email(self, email):
        """
        验证邮箱是否合法
        :param email:
        :return:
        """
        # 邮箱是否已经注册
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError("用户已经存在")  # ValidationError返回400状态码
        # 验证手机号是否合法
        if not re.match(settings.EM_CONF['REGEX_EMAIL'], email):
            raise serializers.ValidationError("邮箱格式错误")

        return email


class PhoneCodeSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True, allow_blank=False, min_length=11, max_length=11,
                                   label='手机号', error_messages={'blank': '手机号不能为空',
                                                                'required': '请输入邮箱',
                                                                "max_length": "手机号长度错误",
                                                                "min_length": "手机号长度错误"})

    def validate_mobile(self, mobile):
        """
        验证手机号是否合法
        :param mobile:
        :return:
        """
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")
        if not re.match(settings.SMS_CONF['REGEX_MOBILE'], mobile):
            raise serializers.ValidationError("手机号格式错误")

        return mobile


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ 自定义JWT令牌声明 """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 向jwt令牌中新增手机号,昵称,邮箱
        token['mobile'] = user.mobile
        token['nickname'] = user.profile.nickname
        token['email'] = user.email
        return token

    # def validate(self, attrs):
    #     data = super().validate(attrs)
    #
    #     refresh = self.get_token(self.user)
    #
    #     data['refresh'] = str(refresh)
    #     data['access'] = str(refresh.access_token)
    #     data['user_id'] = self.user.id
    #     data['mobile'] = self.user.mobile
    #     data['nickname'] = self.user.profile.nickname
    #     data['email'] = self.user.email
    #
    #     if api_settings.UPDATE_LAST_LOGIN:
    #         update_last_login(None, self.user)
    #
    #     return data


class BlacklistRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=625, required=True,
                                          allow_blank=False, write_only=True)

    def validate_refresh_token(self, refresh_token):
        # 通过decode先得到jti
        try:
            payload = refresh_token.split('.')[1]
            payload = decode_base64(payload)
            jti = ast.literal_eval(payload).get('jti', None)
            exp = ast.literal_eval(payload).get('exp', None)
        except Exception as e:
            print(e)
            raise serializers.ValidationError("该令牌格式错误")
        token_qs = OutstandingToken.objects.filter(jti=jti).first()
        if not token_qs:
            raise serializers.ValidationError("该令牌不存在")
        ts = time.time()
        if ts > exp:
            raise serializers.ValidationError('该令牌已过期')
        return refresh_token


class DelUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=625, required=True,
                                          allow_blank=False, write_only=True)
    # todo 2.28
