# apps/monitoring/serializers.py
from rest_framework import serializers
from apps.users.serializers import AddressSerializer
from .models import Region, Plant, Sensor, WaterWell, Dissalinator, Reservoir, SensorReading

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class WaterWellSerializer(serializers.ModelSerializer):
    sensors_detail = SensorSerializer(source='sensors', many=True, read_only=True)
    
    class Meta:
        model = WaterWell
        fields = '__all__'

class DissalinatorSerializer(serializers.ModelSerializer):
    sensors_detail = SensorSerializer(source='sensors', many=True, read_only=True)
    
    class Meta:
        model = Dissalinator
        fields = '__all__'

class ReservoirSerializer(serializers.ModelSerializer):
    sensors_detail = SensorSerializer(source='sensors', many=True, read_only=True)
    
    class Meta:
        model = Reservoir
        fields = '__all__'

class PlantSerializer(serializers.ModelSerializer):
    address_detail = AddressSerializer(source='address', read_only=True)
    region_detail = RegionSerializer(source='region', read_only=True)
    water_well_detail = WaterWellSerializer(source='water_well', read_only=True)
    dissalinator_detail = DissalinatorSerializer(source='dissalinator', read_only=True)
    reservoir_detail = ReservoirSerializer(source='reservoir', read_only=True)
    
    class Meta:
        model = Plant
        fields = '__all__'

class SensorReadingSerializer(serializers.ModelSerializer):
    sensor_detail = SensorSerializer(source='sensor', read_only=True)
    
    class Meta:
        model = SensorReading
        fields = '__all__'