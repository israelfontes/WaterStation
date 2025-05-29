from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

router = DefaultRouter()
router.register('regions', views.RegionViewSet)
router.register('plants', views.PlantViewSet)
router.register('sensors', views.SensorViewSet)
router.register('water-wells', views.WaterWellViewSet)
router.register('dissalinator', views.DissalinatorViewSet)
router.register('reservoirs', views.ReservoirViewSet)
router.register('readings', views.SensorReadingViewSet)

urlpatterns = [
    # APIs padrão do sistema (CRUD completo)
    path('', include(router.urls)),
    
    # APIs específicas para sensores IoT
    
    # Envio de dados
    path('sensor-data/', api_views.sensor_data_single, name='sensor_data_single'),
    path('sensor-data-batch/', api_views.sensor_data_batch, name='sensor_data_batch'),
    path('components/<str:component_type>/<int:component_id>/sensors-data/', 
         api_views.component_sensors_data, name='component_sensors_data'),
    
    # Consulta de informações
    path('sensor/<int:sensor_id>/info/', api_views.sensor_info, name='sensor_info'),
    path('sensor/<int:sensor_id>/readings/', api_views.sensor_readings_history, name='sensor_readings_history'),
    path('components/<str:component_type>/<int:component_id>/sensors/', 
         api_views.component_sensors_list, name='component_sensors_list'),
    
    # Status da API (deve ser o último para evitar conflitos)
    path('health/', api_views.sensor_health_check, name='sensor_health_check'),
]