from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Region, Plant, Sensor, WaterWell, Dissalinator, Reservoir, SensorReading
from .forms import PlantCompleteForm, PlantSimpleForm
from .serializers import (
    RegionSerializer, PlantSerializer, SensorSerializer, 
    WaterWellSerializer, DissalinatorSerializer, ReservoirSerializer, 
    SensorReadingSerializer
)

def check_plant_permission(user):
    """Verifica se o usuário tem permissão para gerenciar plantas"""
    return (user.is_superuser or 
            user.is_staff or 
            (user.auth_level and user.auth_level.name in ['Admin', 'Operador']))

# Web Views
@login_required
def plant_list(request):
    plants = Plant.objects.all().select_related('region', 'address').order_by('-created_at')
    
    # Aplicar filtros se fornecidos
    search = request.GET.get('search')
    plant_type = request.GET.get('type')
    region_id = request.GET.get('region')
    status = request.GET.get('status')
    
    if search:
        plants = plants.filter(name__icontains=search)
    
    if plant_type:
        plants = plants.filter(plant_type=plant_type)
    
    if region_id:
        plants = plants.filter(region_id=region_id)
    
    if status == 'active':
        plants = plants.filter(is_active=True)
    elif status == 'inactive':
        plants = plants.filter(is_active=False)
    
    # Estatísticas
    all_plants = Plant.objects.all()
    active_plants = all_plants.filter(is_active=True).count()
    inactive_plants = all_plants.filter(is_active=False).count()
    total_regions = Region.objects.count()
    
    # Regiões únicas para o filtro
    regions_for_filter = Region.objects.filter(plant__isnull=False).distinct()
    
    context = {
        'plants': plants,
        'total_plants': all_plants.count(),
        'active_plants': active_plants,
        'inactive_plants': inactive_plants,
        'total_regions': total_regions,
        'regions_for_filter': regions_for_filter,
        'can_manage': check_plant_permission(request.user)
    }
    return render(request, 'monitoring/plant_list.html', context)

@login_required
def plant_create(request):
    # Verificar permissões
    if not check_plant_permission(request.user):
        raise PermissionDenied("Você não tem permissão para criar plantas.")
    
    if request.method == 'POST':
        # Verificar se é formulário simples ou completo
        if 'simple_form' in request.POST:
            # Usar formulário simples
            form = PlantSimpleForm(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        plant = form.save()
                        messages.success(request, f'Planta {plant.name} criada com sucesso!')
                        return redirect('plant_detail', pk=plant.pk)
                except Exception as e:
                    messages.error(request, f'Erro ao criar planta: {str(e)}')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        else:
            # Usar formulário completo
            complete_form = PlantCompleteForm(request.POST)
            if complete_form.is_valid():
                try:
                    with transaction.atomic():
                        plant = complete_form.save()
                        messages.success(request, f'Planta {plant.name} criada com sucesso!')
                        return redirect('plant_detail', pk=plant.pk)
                except Exception as e:
                    messages.error(request, f'Erro ao criar planta: {str(e)}')
            else:
                messages.error(request, 'Por favor, corrija os erros no formulário.')
    
    # GET - Mostrar formulários
    regions = Region.objects.all()
    simple_form = PlantSimpleForm()
    complete_form = PlantCompleteForm()
    
    context = {
        'regions': regions,
        'simple_form': simple_form,
        'complete_form': complete_form,
        'title': 'Criar Nova Planta'
    }
    return render(request, 'monitoring/plant_form.html', context)

@login_required
def plant_edit(request, pk):
    # Verificar permissões
    if not check_plant_permission(request.user):
        raise PermissionDenied("Você não tem permissão para editar plantas.")
    
    plant = get_object_or_404(Plant, pk=pk)
    
    if request.method == 'POST':
        complete_form = PlantCompleteForm(request.POST, instance=plant)
        if complete_form.is_valid():
            try:
                with transaction.atomic():
                    updated_plant = complete_form.save()
                    messages.success(request, f'Planta {updated_plant.name} atualizada com sucesso!')
                    return redirect('plant_detail', pk=updated_plant.pk)
            except Exception as e:
                messages.error(request, f'Erro ao atualizar planta: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        complete_form = PlantCompleteForm(instance=plant)
    
    context = {
        'plant': plant,
        'complete_form': complete_form,
        'title': f'Editar Planta - {plant.name}',
        'is_edit': True
    }
    return render(request, 'monitoring/plant_form.html', context)

@login_required
def plant_delete(request, pk):
    # Verificar permissões
    if not check_plant_permission(request.user):
        raise PermissionDenied("Você não tem permissão para remover plantas.")
    
    plant = get_object_or_404(Plant, pk=pk)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                plant_name = plant.name
                
                # Deletar sensores primeiro (para evitar problemas de FK)
                plant.water_well.sensors.all().delete()
                plant.dissalinator.sensors.all().delete()
                plant.reservoir.sensors.all().delete()
                
                # Deletar componentes
                plant.water_well.delete()
                plant.dissalinator.delete()
                plant.reservoir.delete()
                
                # Deletar endereço
                if plant.address:
                    plant.address.delete()
                
                # Deletar planta
                plant.delete()
                
                messages.success(request, f'Planta {plant_name} removida com sucesso!')
                return redirect('plant_list')
        except Exception as e:
            messages.error(request, f'Erro ao remover planta: {str(e)}')
            return redirect('plant_detail', pk=plant.pk)
    
    # Verificar se há leituras de sensores (para alertar o usuário)
    total_readings = 0
    sensors_with_data = []
    
    for sensor in plant.water_well.sensors.all():
        count = sensor.readings.count()
        if count > 0:
            sensors_with_data.append({'name': sensor.name, 'count': count})
            total_readings += count
    
    for sensor in plant.dissalinator.sensors.all():
        count = sensor.readings.count()
        if count > 0:
            sensors_with_data.append({'name': sensor.name, 'count': count})
            total_readings += count
    
    for sensor in plant.reservoir.sensors.all():
        count = sensor.readings.count()
        if count > 0:
            sensors_with_data.append({'name': sensor.name, 'count': count})
            total_readings += count
    
    context = {
        'plant': plant,
        'total_readings': total_readings,
        'sensors_with_data': sensors_with_data,
    }
    return render(request, 'monitoring/plant_confirm_delete.html', context)

@login_required
def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    
    # Buscar últimas leituras dos sensores
    water_well_readings = []
    dissalinator_readings = []
    reservoir_readings = []
    
    # Leituras do poço
    for sensor in plant.water_well.sensors.filter(is_active=True):
        latest_reading = sensor.readings.first()
        if latest_reading:
            water_well_readings.append({
                'sensor': sensor,
                'reading': latest_reading
            })
    
    # Leituras do dessalinizador
    for sensor in plant.dissalinator.sensors.filter(is_active=True):
        latest_reading = sensor.readings.first()
        if latest_reading:
            dissalinator_readings.append({
                'sensor': sensor,
                'reading': latest_reading
            })
    
    # Leituras do reservatório
    for sensor in plant.reservoir.sensors.filter(is_active=True):
        latest_reading = sensor.readings.first()
        if latest_reading:
            reservoir_readings.append({
                'sensor': sensor,
                'reading': latest_reading
            })
    
    # Estatísticas da planta
    total_sensors = (
        plant.water_well.sensors.filter(is_active=True).count() +
        plant.dissalinator.sensors.filter(is_active=True).count() +
        plant.reservoir.sensors.filter(is_active=True).count()
    )
    
    # Verificar alertas (sensores fora da faixa)
    alerts = []
    
    def check_sensor_alerts(readings, component_name):
        for reading_data in readings:
            sensor = reading_data['sensor']
            reading = reading_data['reading']
            
            if sensor.max_value and reading.value > sensor.max_value:
                alerts.append({
                    'type': 'danger',
                    'component': component_name,
                    'message': f'{sensor.name}: {reading.value} {sensor.unit} (máx: {sensor.max_value})'
                })
            elif sensor.min_value and reading.value < sensor.min_value:
                alerts.append({
                    'type': 'warning',
                    'component': component_name,
                    'message': f'{sensor.name}: {reading.value} {sensor.unit} (mín: {sensor.min_value})'
                })
    
    check_sensor_alerts(water_well_readings, 'Poço')
    check_sensor_alerts(dissalinator_readings, 'Dessalinizador')
    check_sensor_alerts(reservoir_readings, 'Reservatório')
    
    context = {
        'plant': plant,
        'water_well_readings': water_well_readings,
        'dissalinator_readings': dissalinator_readings,
        'reservoir_readings': reservoir_readings,
        'total_sensors': total_sensors,
        'alerts': alerts,
        'can_manage': check_plant_permission(request.user)
    }
    return render(request, 'monitoring/plant_detail.html', context)

@login_required
def plant_toggle_status(request, pk):
    """Toggle status ativo/inativo da planta"""
    if not check_plant_permission(request.user):
        raise PermissionDenied("Você não tem permissão para alterar o status das plantas.")
    
    plant = get_object_or_404(Plant, pk=pk)
    
    if request.method == 'POST':
        plant.is_active = not plant.is_active
        plant.save()
        
        status_text = "ativada" if plant.is_active else "desativada"
        messages.success(request, f'Planta {plant.name} foi {status_text}!')
    
    return redirect('plant_detail', pk=pk)

# API ViewSets (mantidas as existentes)
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
        
        for sensor in plant.water_well.sensors.filter(is_active=True):
            latest_reading = sensor.readings.first()
            if latest_reading:
                water_well_readings.append({
                    'sensor': sensor.name,
                    'value': latest_reading.value,
                    'unit': sensor.unit,
                    'timestamp': latest_reading.timestamp
                })
        
        for sensor in plant.dissalinator.sensors.filter(is_active=True):
            latest_reading = sensor.readings.first()
            if latest_reading:
                dissalinator_readings.append({
                    'sensor': sensor.name,
                    'value': latest_reading.value,
                    'unit': sensor.unit,
                    'timestamp': latest_reading.timestamp
                })
        
        for sensor in plant.reservoir.sensors.filter(is_active=True):
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
            'is_active': plant.is_active,
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