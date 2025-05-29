from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
import random
from datetime import datetime, timedelta

from apps.users.models import Address, AuthorizationLevel
from apps.monitoring.models import (
    Region, Plant, Sensor, WaterWell, Dissalinator, 
    Reservoir, SensorReading
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Popular dados de teste para o sistema'

    def handle(self, *args, **options):
        self.stdout.write('Populando dados de teste...')
        
        # Criar endereços de exemplo
        addresses_data = [
            {
                'street': 'Rua das Flores',
                'number': '123',
                'neighborhood': 'Centro',
                'city': 'Mossoró',
                'state': 'RN',
                'cep': '59600-000',
                'latitude': Decimal('-5.1880'),
                'longitude': Decimal('-37.3441')
            },
            {
                'street': 'Av. Presidente Vargas',
                'number': '456',
                'neighborhood': 'Lagoa Nova',
                'city': 'Natal',
                'state': 'RN',
                'cep': '59075-000',
                'latitude': Decimal('-5.7945'),
                'longitude': Decimal('-35.2110')
            }
        ]
        
        addresses = []
        for addr_data in addresses_data:
            address, created = Address.objects.get_or_create(
                street=addr_data['street'],
                number=addr_data['number'],
                defaults=addr_data
            )
            addresses.append(address)
            if created:
                self.stdout.write(f'Endereço criado: {address}')
        
        # Criar usuários de teste
        auth_levels = AuthorizationLevel.objects.all()
        operador_level = auth_levels.filter(name='Operador').first()
        visualizador_level = auth_levels.filter(name='Visualizador').first()
        
        test_users = [
            {
                'username': 'operador1',
                'email': 'operador1@waterstation.com',
                'password': 'op123456',
                'first_name': 'João',
                'last_name': 'Silva',
                'auth_level': operador_level,
                'phone': '(84) 99999-1111'
            },
            {
                'username': 'visualizador1',
                'email': 'visualizador1@waterstation.com', 
                'password': 'vis123456',
                'first_name': 'Maria',
                'last_name': 'Santos',
                'auth_level': visualizador_level,
                'phone': '(84) 99999-2222'
            }
        ]
        
        for user_data in test_users:
            if not User.objects.filter(email=user_data['email']).exists():
                user = User.objects.create_user(**user_data)
                self.stdout.write(f'Usuário criado: {user.email}')
        
        # Criar plantas de exemplo
        regions = Region.objects.all()
        sensors = list(Sensor.objects.all())
        
        if regions.exists() and addresses and sensors:
            # Criar componentes para planta 1
            water_well_1 = WaterWell.objects.create(
                name='Poço Artesiano 001',
                depth=Decimal('150.00')
            )
            water_well_1.sensors.set(sensors[:3])  # Primeiros 3 sensores
            
            dissalinator_1 = Dissalinator.objects.create(
                name='Dessalinizador RO-500',
                capacity=Decimal('500.00')
            )
            dissalinator_1.sensors.set(sensors[2:5])  # Sensores 3-5
            
            reservoir_1 = Reservoir.objects.create(
                name='Reservatório Central',
                capacity=Decimal('10000.00')
            )
            reservoir_1.sensors.set(sensors[4:])  # Últimos sensores
            
            # Criar planta 1
            plant_1 = Plant.objects.create(
                name='Estação Mossoró Norte',
                plant_type='medium',
                address=addresses[0],
                region=regions.first(),
                water_well=water_well_1,
                dissalinator=dissalinator_1,
                reservoir=reservoir_1
            )
            
            self.stdout.write(f'Planta criada: {plant_1.name}')
            
            # Criar leituras de exemplo para os sensores
            self.create_sample_readings(sensors[:6])  # Sensores da primeira planta
        
        self.stdout.write(
            self.style.SUCCESS('Dados de teste populados com sucesso!')
        )
    
    def create_sample_readings(self, sensors):
        """Criar leituras de exemplo para os sensores"""
        
        # Definir ranges de valores por tipo de sensor
        sensor_ranges = {
            'temperature': (20.0, 35.0),
            'ph': (6.5, 8.5),
            'salinity': (100, 1000),
            'flow': (50, 500),
            'pressure': (1.0, 5.0),
            'level': (0, 100)
        }
        
        # Criar leituras para os últimos 7 dias
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        for sensor in sensors:
            if sensor.sensor_type in sensor_ranges:
                min_val, max_val = sensor_ranges[sensor.sensor_type]
                
                # Criar 20-30 leituras aleatórias
                num_readings = random.randint(20, 30)
                
                for i in range(num_readings):
                    # Data aleatória nos últimos 7 dias
                    random_date = start_date + timedelta(
                        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
                    )
                    
                    # Valor aleatório dentro do range
                    value = Decimal(str(round(random.uniform(min_val, max_val), 2)))
                    
                    reading = SensorReading.objects.create(
                        sensor=sensor,
                        value=value,
                        timestamp=random_date
                    )
                
                self.stdout.write(f'Leituras criadas para sensor: {sensor.name}')

# Arquivo de configuração adicional: .env.example
"""
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
"""