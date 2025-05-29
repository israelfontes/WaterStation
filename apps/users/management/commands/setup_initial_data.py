from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.users.models import AuthorizationLevel, Address
from apps.monitoring.models import Region, Sensor, WaterWell, Dissalinator, Reservoir

User = get_user_model()

class Command(BaseCommand):
    help = 'Configura dados iniciais do sistema'

    def handle(self, *args, **options):
        self.stdout.write('Configurando dados iniciais...')
        
        # Criar níveis de autorização
        auth_levels = [
            {'name': 'Admin', 'description': 'Administrador do sistema'},
            {'name': 'Operador', 'description': 'Operador de planta'},
            {'name': 'Visualizador', 'description': 'Apenas visualização'},
        ]
        
        for level_data in auth_levels:
            level, created = AuthorizationLevel.objects.get_or_create(
                name=level_data['name'],
                defaults={'description': level_data['description']}
            )
            if created:
                self.stdout.write(f'Nível de autorização criado: {level.name}')
        
        # Criar regiões
        regions = [
            {'name': 'Agreste', 'description': 'Plantas da região do Agreste'},
            {'name': 'Seridó', 'description': 'Plantas da região do Seridó'},
            {'name': 'Trairi', 'description': 'Plantas da região do Trairi'},
        ]
        
        for region_data in regions:
            region, created = Region.objects.get_or_create(
                name=region_data['name'],
                defaults={'description': region_data['description']}
            )
            if created:
                self.stdout.write(f'Região criada: {region.name}')
        
        # Criar componentes básicos primeiro
        water_wells = [
            {'name': 'Poço Artesiano 001', 'depth': 150.00},
            {'name': 'Poço Artesiano 002', 'depth': 120.00},
        ]
        
        for well_data in water_wells:
            well, created = WaterWell.objects.get_or_create(
                name=well_data['name'],
                defaults={'depth': well_data['depth']}
            )
            if created:
                self.stdout.write(f'Poço criado: {well.name}')
        
        dissalinators = [
            {'name': 'Dessalinizador RO-500', 'capacity': 500.00},
            {'name': 'Dessalinizador RO-1000', 'capacity': 1000.00},
        ]
        
        for diss_data in dissalinators:
            diss, created = Dissalinator.objects.get_or_create(
                name=diss_data['name'],
                defaults={'capacity': diss_data['capacity']}
            )
            if created:
                self.stdout.write(f'Dessalinizador criado: {diss.name}')
        
        reservoirs = [
            {'name': 'Reservatório Central', 'capacity': 10000.00},
            {'name': 'Reservatório Secundário', 'capacity': 5000.00},
        ]
        
        for res_data in reservoirs:
            res, created = Reservoir.objects.get_or_create(
                name=res_data['name'],
                defaults={'capacity': res_data['capacity']}
            )
            if created:
                self.stdout.write(f'Reservatório criado: {res.name}')
        
        # Agora criar sensores associados aos componentes
        # Buscar componentes criados
        water_well_1 = WaterWell.objects.get(name='Poço Artesiano 001')
        dissalinator_1 = Dissalinator.objects.get(name='Dessalinizador RO-500')
        reservoir_1 = Reservoir.objects.get(name='Reservatório Central')
        
        # Sensores para o poço
        well_sensors = [
            {'name': 'Sensor Temperatura Poço 001', 'sensor_type': 'temperature', 'unit': '°C', 'min_value': 15.0, 'max_value': 35.0},
            {'name': 'Sensor pH Poço 001', 'sensor_type': 'ph', 'unit': 'pH', 'min_value': 6.0, 'max_value': 8.5},
            {'name': 'Sensor Salinidade Poço 001', 'sensor_type': 'salinity', 'unit': 'ppm', 'min_value': 0, 'max_value': 2000},
        ]
        
        for sensor_data in well_sensors:
            sensor, created = Sensor.objects.get_or_create(
                name=sensor_data['name'],
                defaults={
                    'sensor_type': sensor_data['sensor_type'],
                    'unit': sensor_data['unit'],
                    'min_value': sensor_data.get('min_value'),
                    'max_value': sensor_data.get('max_value'),
                    'water_well': water_well_1
                }
            )
            if created:
                self.stdout.write(f'Sensor criado: {sensor.name}')
        
        # Sensores para o dessalinizador
        diss_sensors = [
            {'name': 'Sensor Fluxo Dessalinizador RO-500', 'sensor_type': 'flow', 'unit': 'L/h', 'min_value': 0, 'max_value': 600},
            {'name': 'Sensor Pressão Dessalinizador RO-500', 'sensor_type': 'pressure', 'unit': 'bar', 'min_value': 0, 'max_value': 10},
        ]
        
        for sensor_data in diss_sensors:
            sensor, created = Sensor.objects.get_or_create(
                name=sensor_data['name'],
                defaults={
                    'sensor_type': sensor_data['sensor_type'],
                    'unit': sensor_data['unit'],
                    'min_value': sensor_data.get('min_value'),
                    'max_value': sensor_data.get('max_value'),
                    'dissalinator': dissalinator_1
                }
            )
            if created:
                self.stdout.write(f'Sensor criado: {sensor.name}')
        
        # Sensores para o reservatório
        res_sensors = [
            {'name': 'Sensor Nível Reservatório Central', 'sensor_type': 'level', 'unit': '%', 'min_value': 0, 'max_value': 100},
            {'name': 'Sensor Temperatura Reservatório Central', 'sensor_type': 'temperature', 'unit': '°C', 'min_value': 10, 'max_value': 30},
        ]
        
        for sensor_data in res_sensors:
            sensor, created = Sensor.objects.get_or_create(
                name=sensor_data['name'],
                defaults={
                    'sensor_type': sensor_data['sensor_type'],
                    'unit': sensor_data['unit'],
                    'min_value': sensor_data.get('min_value'),
                    'max_value': sensor_data.get('max_value'),
                    'reservoir': reservoir_1
                }
            )
            if created:
                self.stdout.write(f'Sensor criado: {sensor.name}')
        
        # Criar usuário admin se não existir
        admin_level = AuthorizationLevel.objects.get(name='Admin')
        
        if not User.objects.filter(email='admin@waterstation.com').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@waterstation.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                auth_level=admin_level,
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(f'Usuário admin criado: {admin_user.email}')
        
        self.stdout.write(
            self.style.SUCCESS('Dados iniciais configurados com sucesso!')
        )