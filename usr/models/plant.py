from django.db import models
from .address import Address
from .region import Region

class Plant(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Ativo'),
        ('INACTIVE', 'Inativo'),
        ('MAINTENANCE', 'Manutenção'),
    ]
    
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.OneToOneField(Address, on_delete=models.PROTECT)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='ACTIVE'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Plant'
        verbose_name = 'Estação'
        verbose_name_plural = 'Estações'
    
    def __str__(self):
        return f"{self.name or self.type} - {self.region.name}"