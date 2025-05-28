from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('regions', views.RegionViewSet)
router.register('plants', views.PlantViewSet)
router.register('sensors', views.SensorViewSet)
router.register('water-wells', views.WaterWellViewSet)
router.register('dissalinators', views.DissalinatorViewSet)
router.register('reservoirs', views.ReservoirViewSet)
router.register('readings', views.SensorReadingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]