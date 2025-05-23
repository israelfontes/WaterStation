# usr/models/authorization_level.py
from django.db import models

class AuthorizationLevel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    class Meta:
        db_table = 'AuthorizationLevel'
        verbose_name = 'Nível de Autorização'
        verbose_name_plural = 'Níveis de Autorização'
    
    def __str__(self):
        return self.name