# usr/models/sensor.py
from django.db import models

class Sensor(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Ativo'),
        ('INACTIVE', 'Inativo'),
        ('MAINTENANCE', 'Manutenção'),
    ]
    
    type = models.CharField(max_length=255)  # Nível, Vazão, pH
    name = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255, unique=True, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='ACTIVE')
    installation_date = models.DateField(blank=True, null=True)
    calibration_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Sensor'
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensores'
    
    def __str__(self):
        return f"{self.name or self.type} - {self.serial_number}"