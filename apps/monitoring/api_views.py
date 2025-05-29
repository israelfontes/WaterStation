# apps/monitoring/api_views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from decimal import Decimal, InvalidOperation
import json
from datetime import datetime
from .models import Sensor, SensorReading, Plant, WaterWell, Dissalinator, Reservoir
from .serializers import SensorReadingSerializer

# ============================================================================
# ENDPOINTS PARA RECEBER DADOS DOS SENSORES IoT
# ============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sensor_data_single(request):
    """
    API para receber dados de um único sensor
    
    POST /api/monitoring/sensor-data/
    {
        "sensor_id": 1,
        "value": 25.5,
        "timestamp": "2025-05-28T10:30:00Z"  # opcional
    }
    """
    try:
        data = request.data
        
        # Validar campos obrigatórios
        if 'sensor_id' not in data or 'value' not in data:
            return Response({
                'error': 'Campos obrigatórios: sensor_id, value',
                'required_fields': ['sensor_id', 'value'],
                'optional_fields': ['timestamp']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar sensor
        try:
            sensor = Sensor.objects.get(id=data['sensor_id'], is_active=True)
        except Sensor.DoesNotExist:
            return Response({
                'error': f'Sensor {data["sensor_id"]} não encontrado ou inativo'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Validar e converter valor
        try:
            value = Decimal(str(data['value']))
        except (ValueError, TypeError, InvalidOperation):
            return Response({
                'error': 'Valor inválido. Deve ser um número.',
                'received_value': data['value']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar timestamp se fornecido
        timestamp = timezone.now()
        if 'timestamp' in data and data['timestamp']:
            try:
                timestamp = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return Response({
                    'error': 'Timestamp inválido. Use formato ISO 8601 (ex: 2025-05-28T10:30:00Z)'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar range do sensor
        alert_status = 'normal'
        warning_message = None
        
        if sensor.min_value is not None and value < sensor.min_value:
            alert_status = 'below_min'
            warning_message = f'Valor {value} abaixo do mínimo ({sensor.min_value})'
        elif sensor.max_value is not None and value > sensor.max_value:
            alert_status = 'above_max'
            warning_message = f'Valor {value} acima do máximo ({sensor.max_value})'
        
        # Criar leitura
        with transaction.atomic():
            reading = SensorReading.objects.create(
                sensor=sensor,
                value=value,
                timestamp=timestamp
            )
        
        # Obter informações do componente
        component_info = sensor.get_component()
        
        response_data = {
            'success': True,
            'reading_id': reading.id,
            'sensor': {
                'id': sensor.id,
                'name': sensor.name,
                'type': sensor.sensor_type,
                'unit': sensor.unit
            },
            'component': component_info,
            'value': float(value),
            'timestamp': reading.timestamp.isoformat(),
            'status': alert_status
        }
        
        # Adicionar warning se necessário
        if warning_message:
            response_data['warning'] = warning_message
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Erro interno do servidor: {str(e)}',
            'type': 'internal_error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sensor_data_batch(request):
    """
    API para receber dados de múltiplos sensores em lote
    
    POST /api/monitoring/sensor-data-batch/
    {
        "readings": [
            {
                "sensor_id": 1,
                "value": 25.5,
                "timestamp": "2025-05-28T10:30:00Z"
            },
            {
                "sensor_id": 2,
                "value": 7.2
            }
        ]
    }
    """
    try:
        data = request.data
        
        if 'readings' not in data or not isinstance(data['readings'], list):
            return Response({
                'error': 'Campo obrigatório: readings (deve ser um array)',
                'example': {
                    'readings': [
                        {'sensor_id': 1, 'value': 25.5},
                        {'sensor_id': 2, 'value': 7.2}
                    ]
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(data['readings']) == 0:
            return Response({
                'error': 'Array de readings não pode estar vazio'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        results = []
        created_readings = []
        errors = []
        
        with transaction.atomic():
            for i, reading_data in enumerate(data['readings']):
                try:
                    # Validar campos obrigatórios
                    if 'sensor_id' not in reading_data or 'value' not in reading_data:
                        errors.append({
                            'index': i,
                            'error': 'Campos obrigatórios: sensor_id, value',
                            'received': reading_data
                        })
                        continue
                    
                    # Buscar sensor
                    try:
                        sensor = Sensor.objects.get(id=reading_data['sensor_id'], is_active=True)
                    except Sensor.DoesNotExist:
                        errors.append({
                            'index': i,
                            'error': f'Sensor {reading_data["sensor_id"]} não encontrado ou inativo'
                        })
                        continue
                    
                    # Validar valor
                    try:
                        value = Decimal(str(reading_data['value']))
                    except (ValueError, TypeError, InvalidOperation):
                        errors.append({
                            'index': i,
                            'error': f'Valor inválido: {reading_data["value"]}'
                        })
                        continue
                    
                    # Validar timestamp
                    timestamp = timezone.now()
                    if 'timestamp' in reading_data and reading_data['timestamp']:
                        try:
                            timestamp = datetime.fromisoformat(reading_data['timestamp'].replace('Z', '+00:00'))
                        except (ValueError, AttributeError):
                            errors.append({
                                'index': i,
                                'error': f'Timestamp inválido: {reading_data["timestamp"]}'
                            })
                            continue
                    
                    # Criar leitura
                    reading = SensorReading.objects.create(
                        sensor=sensor,
                        value=value,
                        timestamp=timestamp
                    )
                    
                    # Verificar alertas
                    alert_status = 'normal'
                    warning = None
                    
                    if sensor.min_value is not None and value < sensor.min_value:
                        alert_status = 'below_min'
                        warning = f'Abaixo do mínimo ({sensor.min_value})'
                    elif sensor.max_value is not None and value > sensor.max_value:
                        alert_status = 'above_max'
                        warning = f'Acima do máximo ({sensor.max_value})'
                    
                    # Obter informações do componente
                    component_info = sensor.get_component()
                    
                    result_item = {
                        'index': i,
                        'reading_id': reading.id,
                        'sensor': {
                            'id': sensor.id,
                            'name': sensor.name,
                            'type': sensor.sensor_type,
                            'unit': sensor.unit
                        },
                        'component': component_info,
                        'value': float(value),
                        'timestamp': reading.timestamp.isoformat(),
                        'status': alert_status
                    }
                    
                    if warning:
                        result_item['warning'] = warning
                    
                    results.append(result_item)
                    created_readings.append(reading)
                    
                except Exception as e:
                    errors.append({
                        'index': i,
                        'error': f'Erro inesperado: {str(e)}'
                    })
        
        return Response({
            'success': True,
            'summary': {
                'total_sent': len(data['readings']),
                'total_created': len(created_readings),
                'total_errors': len(errors)
            },
            'results': results,
            'errors': errors,
            'timestamp': timezone.now().isoformat()
        }, status=status.HTTP_201_CREATED if created_readings else status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'error': f'Erro interno do servidor: {str(e)}',
            'type': 'internal_error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def component_sensors_data(request, component_type, component_id):
    """
    API para receber dados de todos os sensores de um componente específico
    
    POST /api/monitoring/components/{component_type}/{component_id}/sensors-data/
    
    component_type: 'water-well', 'dissalinator', 'reservoir'
    component_id: ID do componente
    
    {
        "readings": [
            {"sensor_id": 1, "value": 25.5},
            {"sensor_id": 2, "value": 7.2}
        ]
    }
    """
    try:
        # Mapear tipo de componente
        component_map = {
            'water-well': WaterWell,
            'dissalinator': Dissalinator,
            'reservoir': Reservoir
        }
        
        if component_type not in component_map:
            return Response({
                'error': f'Tipo de componente inválido: {component_type}',
                'valid_types': list(component_map.keys()),
                'example_url': '/api/monitoring/components/water-well/1/sensors-data/'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar componente
        ComponentModel = component_map[component_type]
        try:
            component = ComponentModel.objects.get(id=component_id, is_active=True)
        except ComponentModel.DoesNotExist:
            return Response({
                'error': f'{component_type.replace("-", " ").title()} {component_id} não encontrado ou inativo'
            }, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        if 'readings' not in data or not isinstance(data['readings'], list):
            return Response({
                'error': 'Campo obrigatório: readings (deve ser um array)',
                'example': {
                    'readings': [
                        {'sensor_id': 1, 'value': 25.5},
                        {'sensor_id': 2, 'value': 7.2}
                    ]
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        results = []
        errors = []
        
        with transaction.atomic():
            for i, reading_data in enumerate(data['readings']):
                try:
                    if 'sensor_id' not in reading_data or 'value' not in reading_data:
                        errors.append({
                            'index': i,
                            'error': 'Campos obrigatórios: sensor_id, value'
                        })
                        continue
                    
                    # Verificar se o sensor pertence ao componente
                    try:
                        sensor = component.sensors.get(
                            id=reading_data['sensor_id'],
                            is_active=True
                        )
                    except Sensor.DoesNotExist:
                        errors.append({
                            'index': i,
                            'error': f'Sensor {reading_data["sensor_id"]} não encontrado neste {component_type.replace("-", " ")}'
                        })
                        continue
                    
                    # Validar valor
                    try:
                        value = Decimal(str(reading_data['value']))
                    except (ValueError, TypeError, InvalidOperation):
                        errors.append({
                            'index': i,
                            'error': f'Valor inválido: {reading_data["value"]}'
                        })
                        continue
                    
                    # Validar timestamp
                    timestamp = timezone.now()
                    if 'timestamp' in reading_data and reading_data['timestamp']:
                        try:
                            timestamp = datetime.fromisoformat(reading_data['timestamp'].replace('Z', '+00:00'))
                        except (ValueError, AttributeError):
                            errors.append({
                                'index': i,
                                'error': f'Timestamp inválido: {reading_data["timestamp"]}'
                            })
                            continue
                    
                    # Criar leitura
                    reading = SensorReading.objects.create(
                        sensor=sensor,
                        value=value,
                        timestamp=timestamp
                    )
                    
                    # Verificar alertas
                    alert_status = 'normal'
                    warning = None
                    
                    if sensor.min_value is not None and value < sensor.min_value:
                        alert_status = 'below_min'
                        warning = f'Abaixo do mínimo ({sensor.min_value})'
                    elif sensor.max_value is not None and value > sensor.max_value:
                        alert_status = 'above_max'
                        warning = f'Acima do máximo ({sensor.max_value})'
                    
                    result_item = {
                        'sensor_id': sensor.id,
                        'sensor_name': sensor.name,
                        'sensor_type': sensor.sensor_type,
                        'value': float(value),
                        'unit': sensor.unit,
                        'reading_id': reading.id,
                        'timestamp': reading.timestamp.isoformat(),
                        'status': alert_status
                    }
                    
                    if warning:
                        result_item['warning'] = warning
                    
                    results.append(result_item)
                    
                except Exception as e:
                    errors.append({
                        'index': i,
                        'error': f'Erro inesperado: {str(e)}'
                    })
        
        return Response({
            'success': True,
            'component': {
                'type': component_type,
                'id': component.id,
                'name': component.name
            },
            'summary': {
                'readings_sent': len(data['readings']),
                'readings_processed': len(results),
                'errors_count': len(errors)
            },
            'results': results,
            'errors': errors,
            'timestamp': timezone.now().isoformat()
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Erro interno do servidor: {str(e)}',
            'type': 'internal_error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ============================================================================
# ENDPOINTS PARA CONSULTAR INFORMAÇÕES DOS SENSORES
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sensor_info(request, sensor_id):
    """
    API para obter informações detalhadas de um sensor
    
    GET /api/monitoring/sensor/{sensor_id}/info/
    """
    try:
        sensor = get_object_or_404(Sensor, id=sensor_id)
        component_info = sensor.get_component()
        
        response_data = {
            'sensor_id': sensor.id,
            'name': sensor.name,
            'type': sensor.sensor_type,
            'unit': sensor.unit,
            'min_value': float(sensor.min_value) if sensor.min_value else None,
            'max_value': float(sensor.max_value) if sensor.max_value else None,
            'is_active': sensor.is_active,
            'created_at': sensor.created_at.isoformat(),
            'component': component_info,
            'last_reading': None,
            'readings_count': sensor.readings.count()
        }
        
        # Adicionar última leitura se existir
        if sensor.readings.exists():
            latest = sensor.readings.first()
            response_data['last_reading'] = {
                'value': float(latest.value),
                'timestamp': latest.timestamp.isoformat(),
                'reading_id': latest.id
            }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Erro interno do servidor: {str(e)}',
            'type': 'internal_error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def component_sensors_list(request, component_type, component_id):
    """
    Listar todos os sensores de um componente
    
    GET /api/monitoring/components/{component_type}/{component_id}/sensors/
    """
    try:
        component_map = {
            'water-well': WaterWell,
            'dissalinator': Dissalinator,
            'reservoir': Reservoir
        }
        
        if component_type not in component_map:
            return Response({
                'error': f'Tipo de componente inválido: {component_type}',
                'valid_types': list(component_map.keys())
            }, status=status.HTTP_400_BAD_REQUEST)
        
        ComponentModel = component_map[component_type]
        component = get_object_or_404(ComponentModel, id=component_id)
        
        # Filtrar sensores ativos ou todos baseado no parâmetro
        include_inactive = request.query_params.get('include_inactive', 'false').lower() == 'true'
        
        if include_inactive:
            sensors = component.sensors.all()
        else:
            sensors = component.sensors.filter(is_active=True)
        
        sensors_data = []
        
        for sensor in sensors:
            sensor_data = {
                'id': sensor.id,
                'name': sensor.name,
                'type': sensor.sensor_type,
                'unit': sensor.unit,
                'min_value': float(sensor.min_value) if sensor.min_value else None,
                'max_value': float(sensor.max_value) if sensor.max_value else None,
                'is_active': sensor.is_active,
                'created_at': sensor.created_at.isoformat(),
                'readings_count': sensor.readings.count()
            }
            
            # Adicionar última leitura
            if sensor.readings.exists():
                latest = sensor.readings.first()
                sensor_data['last_reading'] = {
                    'value': float(latest.value),
                    'timestamp': latest.timestamp.isoformat(),
                    'reading_id': latest.id
                }
            else:
                sensor_data['last_reading'] = None
            
            sensors_data.append(sensor_data)
        
        return Response({
            'component': {
                'type': component_type,
                'id': component.id,
                'name': component.name,
                'is_active': component.is_active,
                'created_at': component.created_at.isoformat()
            },
            'sensors_count': len(sensors_data),
            'sensors': sensors_data,
            'timestamp': timezone.now().isoformat()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Erro interno do servidor: {str(e)}',
            'type': 'internal_error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sensor_readings_history(request, sensor_id):
    """
    Obter histórico de leituras de um sensor
    
    GET /api/monitoring/sensor/{sensor_id}/readings/
    
    Query Parameters:
    - limit: número máximo de leituras (padrão: 100, máximo: 1000)
    - start_date: data inicial (ISO format)
    - end_date: data final (ISO format)
    """
    try:
        sensor = get_object_or_404(Sensor, id=sensor_id)
        
        # Parâmetros de query
        limit = min(int(request.query_params.get('limit', 100)), 1000)
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Filtrar leituras
        readings_query = sensor.readings.all()
        
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                readings_query = readings_query.filter(timestamp__gte=start_dt)
            except ValueError:
                return Response({
                    'error': 'start_date inválido. Use formato ISO 8601'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                readings_query = readings_query.filter(timestamp__lte=end_dt)
            except ValueError:
                return Response({
                    'error': 'end_date inválido. Use formato ISO 8601'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        readings = readings_query[:limit]
        
        readings_data = []
        for reading in readings:
            readings_data.append({
                'id': reading.id,
                'value': float(reading.value),
                'timestamp': reading.timestamp.isoformat()
            })
        
        return Response({
            'sensor': {
                'id': sensor.id,
                'name': sensor.name,
                'type': sensor.sensor_type,
                'unit': sensor.unit
            },
            'readings_count': len(readings_data),
            'readings': readings_data,
            'filters': {
                'limit': limit,
                'start_date': start_date,
                'end_date': end_date
            },
            'timestamp': timezone.now().isoformat()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Erro interno do servidor: {str(e)}',
            'type': 'internal_error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ============================================================================
# ENDPOINT DE STATUS E SAÚDE DA API
# ============================================================================

@api_view(['GET'])
def sensor_health_check(request):
    """
    Endpoint público para verificar se a API está funcionando
    (sem autenticação para facilitar testes de conectividade)
    """
    try:
        # Estatísticas básicas do sistema
        stats = {
            'sensors_total': Sensor.objects.count(),
            'sensors_active': Sensor.objects.filter(is_active=True).count(),
            'water_wells': WaterWell.objects.filter(is_active=True).count(),
            'dissalinators': Dissalinator.objects.filter(is_active=True).count(),
            'reservoirs': Reservoir.objects.filter(is_active=True).count(),
            'total_readings': SensorReading.objects.count()
        }
        
        return Response({
            'status': 'online',
            'timestamp': timezone.now().isoformat(),
            'version': '1.0.0',
            'api_name': 'WaterStation IoT API',
            'statistics': stats,
            'endpoints': {
                'single_reading': '/api/monitoring/sensor-data/',
                'batch_readings': '/api/monitoring/sensor-data-batch/',
                'component_readings': '/api/monitoring/components/{type}/{id}/sensors-data/',
                'sensor_info': '/api/monitoring/sensor/{sensor_id}/info/',
                'component_sensors': '/api/monitoring/components/{type}/{id}/sensors/',
                'sensor_history': '/api/monitoring/sensor/{sensor_id}/readings/',
                'health_check': '/api/monitoring/health/'
            },
            'component_types': ['water-well', 'dissalinator', 'reservoir'],
            'sensor_types': ['temperature', 'ph', 'salinity', 'flow', 'pressure', 'level'],
            'authentication': {
                'required': False,
                'message': 'This endpoint is public for connectivity testing'
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'timestamp': timezone.now().isoformat(),
            'error': f'Erro no health check: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)