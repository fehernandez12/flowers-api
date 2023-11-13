from django.urls import include, path
from rest_framework.routers import DefaultRouter
from flowers.views import ImageViewSet

router = DefaultRouter()
router.register('image', ImageViewSet, basename='image')

urlpatterns = [
    path('', include(router.urls)),
]