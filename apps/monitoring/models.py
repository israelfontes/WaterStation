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
    
    def __str__(self):
        return f"{self.name} ({self.sensor_type})"
    
    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensores"

class WaterWell(models.Model):
    name = models.CharField(max_length=100)
    depth = models.DecimalField(max_digits=8, decimal_places=2)
    sensors = models.ManyToManyField(Sensor, blank=True)
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
    sensors = models.ManyToManyField(Sensor, blank=True)
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
    sensors = models.ManyToManyField(Sensor, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Reservatório"
        verbose_name_plural = "Reservatórios"

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
    
    class Meta:
        verbose_name = "Planta de Dessalinização"
        verbose_name_plural = "Plantas de Dessalinização"

class SensorReading(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sensor.name}: {self.value} {self.sensor.unit}"
    
    class Meta:
        verbose_name = "Leitura do Sensor"
        verbose_name_plural = "Leituras dos Sensores"
        ordering = ['-timestamp']