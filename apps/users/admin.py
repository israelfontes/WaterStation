from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Address, AuthorizationLevel

@admin.register(AuthorizationLevel)
class AuthorizationLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['street', 'number', 'neighborhood', 'city', 'state', 'cep']
    list_filter = ['state', 'city']
    search_fields = ['street', 'neighborhood', 'city']

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'auth_level', 'is_active', 'created_at']
    list_filter = ['auth_level', 'is_active', 'is_staff', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('phone', 'address', 'auth_level')
        }),
    )