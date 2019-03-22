# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet ,base_name='user')

urlpatterns = [
    path("", include(router.urls))
]