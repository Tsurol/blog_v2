import ast
import json

from django.db import transaction
from rest_framework import generics
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import mixins, viewsets, status
from rest_framework.exceptions import Throttled
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers import EmailCodeSerializer, PhoneCodeSerializer, MyTokenObtainPairSerializer, \
    BlacklistRefreshSerializer, DelUserSerializer
from authentication.throttle import CodeRateThrottle, LoginRateThrottle
from authentication.utils import verify_code, send_email, send_sms, decode_base64

User = get_user_model()


class EmailCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送邮箱验证码接口
    """
    serializer_class = EmailCodeSerializer
    throttle_classes = [CodeRateThrottle]

    def throttled(self, request, wait):
        """
        重写限流错误信息
        :param request:
        :param wait:
        :return:
        """

        class MyThrottled(Throttled):
            default_detail = '请求被限流,'
            extra_detail_singular = '请等待{wait}秒'
            extra_detail_plural = '请等待{wait}秒'

        raise MyThrottled(wait)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # raise_exception=True：如果is_valid 抛出异常则返回400
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        key = 'code_email:{}'.format(email)
        code = verify_code()
        if not settings.DEBUG:
            email_res = send_email(to_email=email, verify_code=code)
            if email_res['code'] != 0:
                return Response({
                    'email': email,
                    'msg': email_res['msg']
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                cache.set(key, json.dumps(code), 60 * 2)
                return Response({
                    'email': email,
                    'msg': email_res['msg']
                }, status=status.HTTP_201_CREATED)
        else:
            cache.set(key, json.dumps(code), 60 * 2)
            return Response({
                'email': email,
                'code': code
            }, status=status.HTTP_201_CREATED)


class PhoneCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码接口
    """
    serializer_class = PhoneCodeSerializer
    throttle_classes = [CodeRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        key = 'code_mobile:{}'.format(mobile)
        code = verify_code()
        if not settings.DEBUG:
            sms_res = send_sms(text="您的验证码是：{}。请不要把验证码泄露给其他人。".format(code), mobile=mobile)
            if sms_res['code'] != 2:
                return Response({
                    "mobile": mobile,
                    "msg": sms_res["msg"]
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                cache.set(key, json.dumps(code), 60 * 2)
                return Response({
                    "mobile": mobile,
                    "msg": "success"
                }, status=status.HTTP_201_CREATED)
        else:
            cache.set(key, json.dumps(code), 60 * 2)
            return Response({
                'mobile': mobile,
                'code': code
            }, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    throttle_classes = [LoginRateThrottle]


class BlacklistRefreshView(mixins.CreateModelMixin, GenericAPIView):
    """
     为了保证安全退出登录
     1. 尽可能缩短访问令牌的到期时间
     2. 从客户端删除 刷新和访问令牌
     3. 将刷新令牌列入黑名单
     """
    serializer_class = BlacklistRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = RefreshToken(serializer.validated_data['refresh_token'])
        refresh_token.blacklist()
        return Response({
            'msg': '已为您安全退出登录',
        }, status=status.HTTP_201_CREATED)


class DeleteUserView(mixins.CreateModelMixin, GenericAPIView):
    """
    注销用户账号
    1.从客户端删除 刷新和访问令牌
    2.将刷新令牌列入黑名单
    3.将数据库中用户信息逻辑删除
    """
    serializer_class = DelUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data['refresh_token']
        payload = refresh.split('.')[1]
        payload = decode_base64(payload)
        user_id = ast.literal_eval(payload).get('user_id', None)
        user = User.objects.filter(id=user_id, is_active=True).first()
        if not user:
            return Response({
                'msg': '用户不存在'
            }, status=status.HTTP_400_BAD_REQUEST)
        refresh_token = RefreshToken(refresh)
        try:
            with transaction.atomic():
                user.is_active = False
                user.profile.is_valid = False
                user.save()
                user.profile.save()
                refresh_token.blacklist()
        except Exception as e:
            print(e)
            return Response({
                'msg': '注销用户操作失败，请检查服务端',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            'msg': '已成功注销账号',
            'user': user_id
        }, status=status.HTTP_201_CREATED)
