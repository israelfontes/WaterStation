# usr/models/water_well.py
from django.db import models
from .plant import Plant
from .component_type import ComponentType

class WaterWell(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Ativo'),
        ('INACTIVE', 'Inativo'),
        ('MAINTENANCE', 'Manutenção'),
    ]
    
    max_flow = models.IntegerField()
    depth = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    component_type = models.ForeignKey(ComponentType, on_delete=models.PROTECT)
    coordinates = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='ACTIVE')
    installation_date = models.DateField(blank=True, null=True)
    last_maintenance_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'WaterWell'
        verbose_name = 'Poço de Água'
        verbose_name_plural = 'Poços de Água'
    
    def __str__(self):
        return f"Poço - {self.plant.name}"