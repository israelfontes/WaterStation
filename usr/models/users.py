from django.contrib.auth.models import AbstractUser
from django.db import models
from .authorization_level import AuthorizationLevel
from .region import Region

class Users(AbstractUser):
    STATUS_CHOICES = [
        ('ACTIVE', 'Ativo'),
        ('INACTIVE', 'Inativo'),
    ]
    
    name = models.CharField(max_length=255)
    auth_level = models.ForeignKey(
        AuthorizationLevel, 
        on_delete=models.PROTECT,
        verbose_name='Nível de Autorização'
    )
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='ACTIVE'
    )
    regions = models.ManyToManyField(
        Region, 
        through='UserRegion',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return self.name or self.username

class UserRegion(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'UserRegion'
        unique_together = ['user', 'region']