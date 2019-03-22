from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import HelloApiView, UserProfileViewSet, PremiumUserProfileViewSet

router = DefaultRouter()

router.register('profile',UserProfileViewSet)
router.register('premium_profile',PremiumUserProfileViewSet)

urlpatterns = [
    url(r'^hello-view/', HelloApiView.as_view()),
    url(r'', include(router.urls))
]