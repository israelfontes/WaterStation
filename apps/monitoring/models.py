from django.db import models
from apps.users.models import Address

class Region(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Região"
        verbose_name_plural = "Regiões"

class WaterWell(models.Model):
    name = models.CharField(max_length=100)
    depth = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Poço de Água"
        verbose_name_plural = "Poços de Água"

class Dissalinator(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.DecimalField(max_digits=10, decimal_places=2)  # L/h
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Dessalinizador"
        verbose_name_plural = "Dessalinizadores"

class Reservoir(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.DecimalField(max_digits=10, decimal_places=2)  # Litros
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Reservatório"
        verbose_name_plural = "Reservatórios"

class Sensor(models.Model):
    SENSOR_TYPES = [
        ('temperature', 'Temperatura'),
        ('ph', 'pH'),
        ('salinity', 'Salinidade'),
        ('flow', 'Fluxo'),
        ('pressure', 'Pressão'),
        ('level', 'Nível'),
    ]
    
    name = models.CharField(max_length=100)
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    unit = models.CharField(max_length=10)
    min_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Relacionamentos com os componentes (apenas um pode estar preenchido)
    water_well = models.ForeignKey(WaterWell, on_delete=models.CASCADE, null=True, blank=True, related_name='sensors')
    dissalinator = models.ForeignKey(Dissalinator, on_delete=models.CASCADE, null=True, blank=True, related_name='sensors')
    reservoir = models.ForeignKey(Reservoir, on_delete=models.CASCADE, null=True, blank=True, related_name='sensors')
    
    def __str__(self):
        return f"{self.name} ({self.sensor_type})"
    
    def get_component(self):
        """Retorna o componente ao qual o sensor está associado"""
        if self.water_well:
            return {'type': 'water_well', 'name': self.water_well.name, 'id': self.water_well.id}
        elif self.dissalinator:
            return {'type': 'dissalinator', 'name': self.dissalinator.name, 'id': self.dissalinator.id}
        elif self.reservoir:
            return {'type': 'reservoir', 'name': self.reservoir.name, 'id': self.reservoir.id}
        return None
    
    def clean(self):
        """Validação para garantir que apenas um componente seja selecionado"""
        from django.core.exceptions import ValidationError
        
        components = [self.water_well, self.dissalinator, self.reservoir]
        filled_components = [comp for comp in components if comp is not None]
        
        if len(filled_components) == 0:
            raise ValidationError('O sensor deve estar associado a pelo menos um componente (Poço, Dessalinizador ou Reservatório).')
        
        if len(filled_components) > 1:
            raise ValidationError('O sensor pode estar associado a apenas um componente por vez.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensores"

class Plant(models.Model):
    PLANT_TYPES = [
        ('small', 'Pequena'),
        ('medium', 'Média'),
        ('large', 'Grande'),
    ]
    
    name = models.CharField(max_length=100)
    plant_type = models.CharField(max_length=10, choices=PLANT_TYPES)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    water_well = models.OneToOneField(WaterWell, on_delete=models.CASCADE)
    dissalinator = models.OneToOneField(Dissalinator, on_delete=models.CASCADE)
    reservoir = models.OneToOneField(Reservoir, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def get_all_sensors(self):
        """Retorna todos os sensores da planta organizados por componente"""
        return {
            'water_well': list(self.water_well.sensors.filter(is_active=True)),
            'dissalinator': list(self.dissalinator.sensors.filter(is_active=True)),
            'reservoir': list(self.reservoir.sensors.filter(is_active=True))
        }
    
    def get_sensors_count(self):
        """Retorna o total de sensores da planta"""
        return (
            self.water_well.sensors.filter(is_active=True).count() +
            self.dissalinator.sensors.filter(is_active=True).count() +
            self.reservoir.sensors.filter(is_active=True).count()
        )
    
    class Meta:
        verbose_name = "Planta de Dessalinização"
        verbose_name_plural = "Plantas de Dessalinização"

class SensorReading(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sensor.name}: {self.value} {self.sensor.unit}"
    
    def get_component_info(self):
        """Retorna informações do componente associado ao sensor"""
        return self.sensor.get_component()
    
    class Meta:
        verbose_name = "Leitura do Sensor"
        verbose_name_plural = "Leituras dos Sensores"
        ordering = ['-timestamp']