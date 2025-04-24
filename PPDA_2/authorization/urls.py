# authorization/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileTypeModelViewSet

router = DefaultRouter()
router.register(r'profile_types', ProfileTypeModelViewSet, basename='profiletype')

urlpatterns = [
    path('', include(router.urls)),
]