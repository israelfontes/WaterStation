from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    STATUS_CHOICES = [
        ('ACTIVE', 'Ativo'),
        ('INACTIVE', 'Inativo'),
    ]
    
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        verbose_name='Status'
    )
    regions = models.ManyToManyField(
        'Region',
        through='UserRegion',
        blank=True,
        verbose_name='Regiões'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username

class UserRegion(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'UserRegion'
        unique_together = ['user', 'region']

    def __str__(self):
        return f"{self.user.username} -> {self.region.name}"