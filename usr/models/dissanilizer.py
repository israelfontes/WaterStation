# usr/models/dissanilizer.py
from django.db import models
from .plant import Plant
from .component_type import ComponentType

class Dissanilizer(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Ativo'),
        ('INACTIVE', 'Inativo'),
        ('MAINTENANCE', 'Manutenção'),
    ]
    
    max_alkalinity = models.IntegerField()
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    component_type = models.ForeignKey(ComponentType, on_delete=models.PROTECT)
    coordinates = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='ACTIVE')
    installation_date = models.DateField(blank=True, null=True)
    last_maintenance_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Dissanilizer'
        verbose_name = 'Dessalinizador'
        verbose_name_plural = 'Dessalinizadores'
    
    def __str__(self):
        return f"Dessalinizador - {self.plant.name}"