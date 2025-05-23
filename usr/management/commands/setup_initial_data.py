# usr/management/commands/setup_initial_data.py
from django.core.management.base import BaseCommand
from usr.models import AuthorizationLevel, Region, ComponentType

class Command(BaseCommand):
    help = 'Configura dados iniciais do sistema'
    
    def handle(self, *args, **options):
        # Níveis de autorização
        auth_levels = ['ADMIN', 'MANAGER', 'OPERATOR', 'VIEWER']
        for level in auth_levels:
            AuthorizationLevel.objects.get_or_create(name=level)
        
        # Regiões
        regions = [
            ('Norte', 'Região Norte da área de cobertura'),
            ('Sul', 'Região Sul da área de cobertura'),
            ('Leste', 'Região Leste da área de cobertura'),
            ('Oeste', 'Região Oeste da área de cobertura'),
            ('Centro', 'Região Centro da área de cobertura'),
        ]
        for name, desc in regions:
            Region.objects.get_or_create(name=name, defaults={'description': desc})
        
        # Tipos de componentes
        component_types = [
            ('RESERVOIR', 'Reservoir', 'Reservatórios de armazenamento de água'),
            ('DISSANILIZER', 'Dissanilizer', 'Sistemas de dessalinização'),
            ('WATER_WELL', 'WaterWell', 'Poços de água subterrânea'),
        ]
        for name, table, desc in component_types:
            ComponentType.objects.get_or_create(
                name=name, 
                defaults={'table_name': table, 'description': desc}
            )
        
        self.stdout.write(
            self.style.SUCCESS('Dados iniciais configurados com sucesso!')
        )