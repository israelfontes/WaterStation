from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'Region'
        verbose_name = 'Região'
        verbose_name_plural = 'Regiões'
    
    def __str__(self):
        return self.name