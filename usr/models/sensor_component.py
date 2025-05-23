# usr/models/sensor_component.py
from django.db import models
from .sensor import Sensor
from .component_type import ComponentType

class SensorComponent(models.Model):
    sensor = models.OneToOneField(Sensor, on_delete=models.CASCADE)
    component_type = models.ForeignKey(ComponentType, on_delete=models.PROTECT)
    component_id = models.BigIntegerField()  # ID polimórfico
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'SensorComponent'
        verbose_name = 'Sensor-Componente'
        verbose_name_plural = 'Sensores-Componentes'
    
    def __str__(self):
        return f"{self.sensor} -> {self.component_type.name}"

class SensorRead(models.Model):
    STATUS_CHOICES = [
        ('VALID', 'Válido'),
        ('INVALID', 'Inválido'),
        ('ESTIMATED', 'Estimado'),
    ]
    
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='VALID')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'SensorRead'
        verbose_name = 'Leitura do Sensor'
        verbose_name_plural = 'Leituras dos Sensores'
        indexes = [
            models.Index(fields=['sensor', 'datetime']),
            models.Index(fields=['datetime']),
        ]
    
    def __str__(self):
        return f"{self.sensor} - {self.value} {self.unit} ({self.datetime})"