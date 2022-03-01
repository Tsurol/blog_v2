import base64
import random
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
import http.client
import json
from urllib.parse import urlencode

from rest_framework_simplejwt.tokens import RefreshToken


def verify_code():
    """
    生成四位数验证码
    :return:
    """
    seeds = "1234567890"
    random_str = []
    for i in range(4):
        random_str.append(random.choice(seeds))
    return ''.join(random_str)


def send_email(to_email: str, verify_code: str):
    """
    :param to_email: 收件邮箱
    :param verify_code: 验证码
    :return:
    """
    # 邮件主题
    subject = "[周梓凌的个人网站】请查收您的短信登录验证码"
    mail_msg = MIMEMultipart()
    content = '您的邮箱验证码为：{} \n\n\n\n\n\n ---  {}  ---' \
        .format(verify_code, settings.EM_CONF['PROJECT_NAME'])
    mail_msg.attach(MIMEText(content, 'plain', 'utf-8'))
    mail_msg['From'] = settings.EM_CONF['sender_email']
    mail_msg['Subject'] = Header(subject, 'utf-8')
    mail_msg['To'] = to_email
    try:
        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL(settings.EM_CONF['smtp_server'])
        server.connect(settings.EM_CONF['smtp_server'], settings.EM_CONF['port'])
        # 登录发信邮箱
        server.login(settings.EM_CONF['sender_email'], settings.EM_CONF['sender_passwd'])
        # 发送邮件
        server.sendmail(settings.EM_CONF['sender_email'], to_email, mail_msg.as_string())
        # 关闭服务器
        server.quit()
    except smtplib.SMTPException as e:
        return {
            'code': 1,
            'msg': e
        }
    return {
        'code': 0,
        'msg': 'success'
    }


def send_sms(text, mobile):
    """
    发送短信验证码
    :param text:
    :param mobile:
    :return:
    """
    params = urlencode(
        {'account': settings.SMS_CONF['account'], 'password': settings.SMS_CONF['password'], 'content': text,
         'mobile': mobile,
         'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(settings.SMS_CONF['host'], port=80, timeout=30)
    conn.request("POST", settings.SMS_CONF['sms_send_uri'], params, headers)
    response = conn.getresponse()
    response_str = response.read()
    json_str = response_str.decode('utf-8')
    result = json.loads(json_str)
    conn.close()
    return result


User = get_user_model()  # 快捷获取用户模型


class CustomBackend(ModelBackend):
    """ 自定义用户认证 """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 添加了一个手机验证和邮箱验证，如果需要其他验证再加
            user = User.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            print(e)
            return None


def get_tokens_for_user(user):
    """ 手动创建JWT令牌 """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def decode_base64(data):
    """Decode base64, padding being optional.
    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    # base64长度是4的倍数，如果不足，需要用'='补齐
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    return str(base64.b64decode(data),
               encoding='utf-8')
