from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import CustomUser, Address, AuthorizationLevel
from .forms import UserForm, LoginForm
from .serializers import UserSerializer, AddressSerializer, AuthorizationLevelSerializer

# Web Views
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Email ou senha inválidos')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    
    # Verificar se é administrador (apenas Admin, não Operador)
    is_admin = check_admin_permission(user)
    
    if is_admin:
        # Dashboard do Administrador
        from apps.monitoring.models import Plant, Region, Sensor, SensorReading
        
        context = {
            'is_admin': True,
            'total_users': CustomUser.objects.count(),
            'total_plants': Plant.objects.count(),
            'total_regions': Region.objects.count(),
            'total_sensors': Sensor.objects.count(),
            'active_plants': Plant.objects.filter(is_active=True).count(),
            'inactive_plants': Plant.objects.filter(is_active=False).count(),
            'recent_users': CustomUser.objects.order_by('-created_at')[:5],
            'recent_plants': Plant.objects.select_related('region', 'address').order_by('-created_at')[:5],
        }
        return render(request, 'users/dashboard_admin.html', context)
    
    else:
        # Dashboard do Usuário Normal (Operador/Visualizador)
        from apps.monitoring.models import Plant, Region, SensorReading
        from django.db.models import Count, Avg, Max
        from datetime import datetime, timedelta
        
        # Estatísticas das plantas
        plants = Plant.objects.select_related('region', 'address', 'water_well', 'dissalinator', 'reservoir')
        
        # Plantas por região
        plants_by_region = Region.objects.annotate(
            plant_count=Count('plant')
        ).filter(plant_count__gt=0)
        
        # Plantas por tipo
        plants_by_type = Plant.objects.values('plant_type').annotate(
            count=Count('id')
        ).order_by('plant_type')
        
        # Últimas leituras de sensores (últimas 24 horas)
        last_24h = datetime.now() - timedelta(hours=24)
        recent_readings = SensorReading.objects.select_related('sensor').filter(
            timestamp__gte=last_24h
        ).order_by('-timestamp')[:10]
        
        # Estatísticas por tipo de sensor nas últimas 24h
        sensor_stats = SensorReading.objects.filter(
            timestamp__gte=last_24h
        ).values('sensor__sensor_type', 'sensor__unit').annotate(
            avg_value=Avg('value'),
            max_value=Max('value'),
            count=Count('id')
        ).order_by('sensor__sensor_type')
        
        # Plantas com alertas (simulado - sensores fora da faixa normal)
        plants_with_alerts = []
        for plant in plants.filter(is_active=True):
            alerts = []
            
            # Verificar sensores do poço
            for sensor in plant.water_well.sensors.all():
                latest_reading = sensor.readings.first()
                if latest_reading and sensor.max_value and latest_reading.value > sensor.max_value:
                    alerts.append(f"{sensor.name}: {latest_reading.value} {sensor.unit} (máx: {sensor.max_value})")
                elif latest_reading and sensor.min_value and latest_reading.value < sensor.min_value:
                    alerts.append(f"{sensor.name}: {latest_reading.value} {sensor.unit} (mín: {sensor.min_value})")
            
            # Verificar sensores do dessalinizador
            for sensor in plant.dissalinator.sensors.all():
                latest_reading = sensor.readings.first()
                if latest_reading and sensor.max_value and latest_reading.value > sensor.max_value:
                    alerts.append(f"{sensor.name}: {latest_reading.value} {sensor.unit} (máx: {sensor.max_value})")
                elif latest_reading and sensor.min_value and latest_reading.value < sensor.min_value:
                    alerts.append(f"{sensor.name}: {latest_reading.value} {sensor.unit} (mín: {sensor.min_value})")
            
            # Verificar sensores do reservatório
            for sensor in plant.reservoir.sensors.all():
                latest_reading = sensor.readings.first()
                if latest_reading and sensor.max_value and latest_reading.value > sensor.max_value:
                    alerts.append(f"{sensor.name}: {latest_reading.value} {sensor.unit} (máx: {sensor.max_value})")
                elif latest_reading and sensor.min_value and latest_reading.value < sensor.min_value:
                    alerts.append(f"{sensor.name}: {latest_reading.value} {sensor.unit} (mín: {sensor.min_value})")
            
            if alerts:
                plants_with_alerts.append({
                    'plant': plant,
                    'alerts': alerts
                })
        
        context = {
            'is_admin': False,
            'user': user,
            'total_plants': plants.count(),
            'active_plants': plants.filter(is_active=True).count(),
            'inactive_plants': plants.filter(is_active=False).count(),
            'total_regions': Region.objects.count(),
            'plants_by_region': plants_by_region,
            'plants_by_type': plants_by_type,
            'recent_readings': recent_readings,
            'sensor_stats': sensor_stats,
            'plants_with_alerts': plants_with_alerts,
            'recent_plants': plants.order_by('-created_at')[:6],
            # Adicionar informações sobre permissões do usuário
            'can_manage_plants': check_plant_permission(user),
            'user_role': user.auth_level.name if user.auth_level else 'Usuário'
        }
        return render(request, 'users/dashboard_user.html', context)

def check_admin_permission(user):
    """Verifica se o usuário tem permissão de ADMINISTRADOR (apenas Admin)"""
    return (user.is_superuser or 
            user.is_staff or 
            (user.auth_level and user.auth_level.name == 'Admin'))

def check_plant_permission(user):
    """Verifica se o usuário tem permissão para gerenciar PLANTAS (Admin + Operador)"""
    return (user.is_superuser or 
            user.is_staff or 
            (user.auth_level and user.auth_level.name in ['Admin', 'Operador']))

@login_required
def user_list(request):
    # Verificar se é admin
    if not check_admin_permission(request.user):
        raise PermissionDenied("Apenas administradores podem gerenciar usuários.")
    
    users = CustomUser.objects.all().order_by('-created_at')
    return render(request, 'users/user_list.html', {'users': users})

@login_required
def user_create(request):
    # Verificar se é admin
    if not check_admin_permission(request.user):
        raise PermissionDenied("Apenas administradores podem criar usuários.")
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuário {user.email} criado com sucesso!')
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'users/user_form.html', {'form': form, 'title': 'Criar Usuário'})

@login_required
def user_edit(request, pk):
    # Verificar se é admin
    if not check_admin_permission(request.user):
        raise PermissionDenied("Apenas administradores podem editar usuários.")
    
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuário {user.email} atualizado com sucesso!')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'title': 'Editar Usuário'})

@login_required
def user_delete(request, pk):
    # Verificar se é admin
    if not check_admin_permission(request.user):
        raise PermissionDenied("Apenas administradores podem remover usuários.")
    
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        email = user.email
        user.delete()
        messages.success(request, f'Usuário {email} removido com sucesso!')
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})

# API ViewSets
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

class AuthorizationLevelViewSet(viewsets.ModelViewSet):
    queryset = AuthorizationLevel.objects.all()
    serializer_class = AuthorizationLevelSerializer
    permission_classes = [IsAuthenticated]
