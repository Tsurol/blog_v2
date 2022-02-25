from django.urls import path
from rest_framework.routers import DefaultRouter
from authentication.views import EmailCodeViewSet, PhoneCodeViewSet

router = DefaultRouter()
router.register(r'email/code', EmailCodeViewSet, basename='email_code')
router.register(r'phone/code', PhoneCodeViewSet, basename='phone_code')

