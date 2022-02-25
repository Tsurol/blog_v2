from rest_framework.routers import DefaultRouter

from blogsite.views import BlogViewSet, TagViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'blogsite/list', BlogViewSet, basename='blog_list')
router.register(r'tag/list', TagViewSet, basename='tag_list')
router.register(r'comment/list', CommentViewSet, basename='comment_list')
