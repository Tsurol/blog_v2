"""blog_v2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from authentication.views import MyTokenObtainPairView, BlacklistRefreshView, DeleteUserView
from blogsite.urls import router as router_blog
from authentication.urls import router as router_auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/blog/', include(router_blog.urls)),
    path('api/auth/', include(router_auth.urls)),
    path('login/', MyTokenObtainPairView.as_view(), name='jwt_obtain'),
    path('register/', MyTokenObtainPairView.as_view(), name='jwt_obtain'),  # todo 注册 2022/3/7
    path('token/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('logout/', BlacklistRefreshView.as_view(), name='jwt_logout'),
    path('user/del/', DeleteUserView.as_view(), name='jwt_del'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # todo:后期需要改成STATIC_ROOT
    re_path(r'^static/(?P<path>.*)/$', serve, {'document_root': settings.STATICFILES_DIRS}),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
