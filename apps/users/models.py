# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class AuthorizationLevel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Nível de Autorização"
        verbose_name_plural = "Níveis de Autorização"

class Address(models.Model):
    street = models.CharField(max_length=200)
    number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    cep = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}/{self.state}"
    
    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    auth_level = models.ForeignKey(AuthorizationLevel, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"