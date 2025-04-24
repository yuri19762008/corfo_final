
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponseRedirect
from rest_framework import urls as drf_urls
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import OrganismoViewSet, PlanDescontaminacionViewSet, TipoMedidaViewSet, MedidaViewSet, ReporteViewSet

router = DefaultRouter()
#TODO:Cambiar estas urls a la app core.
router.register('plan_descontaminacion', PlanDescontaminacionViewSet)
router.register('organismo', OrganismoViewSet)
router.register('tipo_medida', TipoMedidaViewSet)
router.register('medida', MedidaViewSet)
router.register('reporte',ReporteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/authentication/', include('authentication.urls')),
    path('api/authorization/',include('authorization.urls')),

    # Documentación 
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', lambda request: HttpResponseRedirect('/api/')), #Redirigir todo a API REST

    path('api-auth/', include(drf_urls)),
]+ debug_toolbar_urls()
