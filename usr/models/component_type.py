from django.db import models

class ComponentType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    table_name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ComponentType'
        verbose_name = 'Tipo de Componente'
        verbose_name_plural = 'Tipos de Componentes'
    
    def __str__(self):
        return self.name