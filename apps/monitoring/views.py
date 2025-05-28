from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Region, Plant, Sensor, WaterWell, Dissalinator, Reservoir, SensorReading
from .serializers import (
    RegionSerializer, PlantSerializer, SensorSerializer, 
    WaterWellSerializer, DissalinatorSerializer, ReservoirSerializer, 
    SensorReadingSerializer
)

# Web Views
@login_required
def plant_list(request):
    plants = Plant.objects.all().select_related('region', 'address').order_by('-created_at')
    context = {
        'plants': plants,
        'total_plants': plants.count()
    }
    return render(request, 'monitoring/plant_list.html', context)

@login_required
def plant_create(request):
    if request.method == 'POST':
        # Criar endereço básico
        from apps.users.models import Address
        address = Address.objects.create(
            street=request.POST.get('street', ''),
            number='S/N',
            neighborhood='Centro',
            city=request.POST.get('city', ''),
            state=request.POST.get('state', ''),
            cep='00000-000'
        )
        
        # Criar componentes básicos
        water_well = WaterWell.objects.create(
            name=f"Poço {request.POST.get('plant_name', '')}",
            depth=100.00
        )
        
        dissalinator = Dissalinator.objects.create(
            name=f"Dessalinizador {request.POST.get('plant_name', '')}",
            capacity=500.00
        )
        
        reservoir = Reservoir.objects.create(
            name=f"Reservatório {request.POST.get('plant_name', '')}",
            capacity=10000.00
        )
        
        # Criar planta
        region = Region.objects.get(id=request.POST.get('region'))
        plant = Plant.objects.create(
            name=request.POST.get('plant_name'),
            plant_type=request.POST.get('plant_type'),
            address=address,
            region=region,
            water_well=water_well,
            dissalinator=dissalinator,
            reservoir=reservoir
        )
        
        messages.success(request, f'Planta {plant.name} criada com sucesso!')
        return redirect('plant_detail', pk=plant.pk)
    
    regions = Region.objects.all()
    context = {
        'regions': regions,
        'title': 'Criar Nova Planta'
    }
    return render(request, 'monitoring/plant_form.html', context)

@login_required
def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    
    # Buscar últimas leituras dos sensores
    water_well_readings = []
    dissalinator_readings = []
    reservoir_readings = []
    
    # Leituras do poço
    for sensor in plant.water_well.sensors.all():
        latest_reading = sensor.readings.first()
        if latest_reading:
            water_well_readings.append({
                'sensor': sensor,
                'reading': latest_reading
            })
    
    # Leituras do dessalinizador
    for sensor in plant.dissalinator.sensors.all():
        latest_reading = sensor.readings.first()
        if latest_reading:
            dissalinator_readings.append({
                'sensor': sensor,
                'reading': latest_reading
            })
    
    # Leituras do reservatório
    for sensor in plant.reservoir.sensors.all():
        latest_reading = sensor.readings.first()
        if latest_reading:
            reservoir_readings.append({
                'sensor': sensor,
                'reading': latest_reading
            })
    
    context = {
        'plant': plant,
        'water_well_readings': water_well_readings,
        'dissalinator_readings': dissalinator_readings,
        'reservoir_readings': reservoir_readings,
    }
    return render(request, 'monitoring/plant_detail.html', context)

# API ViewSets
class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated]

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def readings(self, request, pk=None):
        sensor = self.get_object()
        readings = sensor.readings.all()[:100]  # Últimas 100 leituras
        serializer = SensorReadingSerializer(readings, many=True)
        return Response(serializer.data)

class WaterWellViewSet(viewsets.ModelViewSet):
    queryset = WaterWell.objects.all()
    serializer_class = WaterWellSerializer
    permission_classes = [IsAuthenticated]

class DissalinatorViewSet(viewsets.ModelViewSet):
    queryset = Dissalinator.objects.all()
    serializer_class = DissalinatorSerializer
    permission_classes = [IsAuthenticated]

class ReservoirViewSet(viewsets.ModelViewSet):
    queryset = Reservoir.objects.all()
    serializer_class = ReservoirSerializer
    permission_classes = [IsAuthenticated]

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        plant = self.get_object()
        
        # Buscar últimas leituras de cada componente
        water_well_readings = []
        dissalinator_readings = []
        reservoir_readings = []
        
        for sensor in plant.water_well.sensors.all():
            latest_reading = sensor.readings.first()
            if latest_reading:
                water_well_readings.append({
                    'sensor': sensor.name,
                    'value': latest_reading.value,
                    'unit': sensor.unit,
                    'timestamp': latest_reading.timestamp
                })
        
        for sensor in plant.dissalinator.sensors.all():
            latest_reading = sensor.readings.first()
            if latest_reading:
                dissalinator_readings.append({
                    'sensor': sensor.name,
                    'value': latest_reading.value,
                    'unit': sensor.unit,
                    'timestamp': latest_reading.timestamp
                })
        
        for sensor in plant.reservoir.sensors.all():
            latest_reading = sensor.readings.first()
            if latest_reading:
                reservoir_readings.append({
                    'sensor': sensor.name,
                    'value': latest_reading.value,
                    'unit': sensor.unit,
                    'timestamp': latest_reading.timestamp
                })
        
        return Response({
            'plant': plant.name,
            'water_well': water_well_readings,
            'dissalinator': dissalinator_readings,
            'reservoir': reservoir_readings
        })

class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = SensorReading.objects.all()
        sensor_id = self.request.query_params.get('sensor', None)
        if sensor_id is not None:
            queryset = queryset.filter(sensor=sensor_id)
        return queryset.order_by('-timestamp')

