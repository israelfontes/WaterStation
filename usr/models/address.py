from django.db import models
from .users import Users

class Address(models.Model):
    street = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    neighborhood = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    cep = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Address'
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
    
    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}/{self.state}"