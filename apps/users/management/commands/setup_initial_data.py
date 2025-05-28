# apps/users/management/__init__.py
# (arquivo vazio)

# apps/users/management/commands/__init__.py
# (arquivo vazio)

# apps/users/management/commands/setup_initial_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.users.models import AuthorizationLevel, Address
from apps.monitoring.models import Region, Sensor

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
            {'name': 'Agreste', 'description': 'Plantas da região Agreste'},
            {'name': 'Seridó', 'description': 'Plantas da região Seridó'},
            {'name': 'Trairi', 'description': 'Plantas da região Trairi'},
        ]
        
        for region_data in regions:
            region, created = Region.objects.get_or_create(
                name=region_data['name'],
                defaults={'description': region_data['description']}
            )
            if created:
                self.stdout.write(f'Região criada: {region.name}')
        
        # Criar tipos de sensores básicos
        sensors_data = [
            {'name': 'Sensor de Temperatura', 'sensor_type': 'temperature', 'unit': '°C'},
            {'name': 'Sensor de pH', 'sensor_type': 'ph', 'unit': 'pH'},
            {'name': 'Sensor de Salinidade', 'sensor_type': 'salinity', 'unit': 'ppm'},
            {'name': 'Sensor de Fluxo', 'sensor_type': 'flow', 'unit': 'L/h'},
            {'name': 'Sensor de Pressão', 'sensor_type': 'pressure', 'unit': 'bar'},
            {'name': 'Sensor de Nível', 'sensor_type': 'level', 'unit': '%'},
        ]
        
        for sensor_data in sensors_data:
            sensor, created = Sensor.objects.get_or_create(
                name=sensor_data['name'],
                defaults={
                    'sensor_type': sensor_data['sensor_type'],
                    'unit': sensor_data['unit']
                }
            )
            if created:
                self.stdout.write(f'Sensor criado: {sensor.name}')
        
        # Criar usuário admin se não existir
        admin_level = AuthorizationLevel.objects.get(name='Admin')
        
        if not User.objects.filter(email='admin@gmail.com').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@gmail.com',
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