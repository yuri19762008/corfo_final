from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


router = DefaultRouter()
router.register(r'users', views.UserModelViewSet)


urlpatterns = [
    #Incluir rutas del router de autentication para hacer REST.
    path('', include(router.urls)),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
]
