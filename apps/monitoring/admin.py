from django.contrib import admin
from .models import Region, Plant, Sensor, WaterWell, Dissalinator, Reservoir, SensorReading

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['name', 'sensor_type', 'unit', 'is_active', 'created_at']
    list_filter = ['sensor_type', 'is_active']
    search_fields = ['name']

@admin.register(WaterWell)
class WaterWellAdmin(admin.ModelAdmin):
    list_display = ['name', 'depth', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    filter_horizontal = ['sensors']

@admin.register(Dissalinator)
class DissalinatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    filter_horizontal = ['sensors']

@admin.register(Reservoir)
class ReservoirAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    filter_horizontal = ['sensors']

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'plant_type', 'region', 'is_active', 'created_at']
    list_filter = ['plant_type', 'region', 'is_active']
    search_fields = ['name']

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'value', 'timestamp']
    list_filter = ['sensor__sensor_type', 'timestamp']
    search_fields = ['sensor__name']
    date_hierarchy = 'timestamp'