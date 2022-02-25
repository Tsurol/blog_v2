from rest_framework import throttling


class CodeRateThrottle(throttling.SimpleRateThrottle):
    """ 自定义验证码接口节流 """
    # 对应settings内DEFAULT_THROTTLE_RATE的key值，用于获取value
    scope = 'code'

    def get_cache_key(self, request, view):
        # 返回ip地址
        return self.get_ident(request)


class LoginRateThrottle(throttling.SimpleRateThrottle):
    """ 自定义登录接口节流 """
    # 对应settings内DEFAULT_THROTTLE_RATE的key值，用于获取value
    scope = 'login'

    def get_cache_key(self, request, view):
        # 返回ip地址
        return self.get_ident(request)

# class UserThrottle(throttling.SimpleRateThrottle):
#     """ 登录用户节流 """
#     scope = 'userThrottle'
#
#     def get_cache_key(self, request, view):
#         return request.user.user_id
