# usr/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .models import UserRegion

class UserRegionInline(admin.TabularInline):
    model = UserRegion
    extra = 1

@admin.register(AuthorizationLevel)
class AuthorizationLevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']

@admin.register(Users)
class UsersAdmin(UserAdmin):
    inlines = [UserRegionInline]
    list_display = ['username', 'name', 'email', 'auth_level', 'status']
    list_filter = ['auth_level', 'status', 'is_staff']
    search_fields = ['username', 'name', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('name', 'auth_level', 'status')
        }),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'street', 'city', 'state', 'user']
    list_filter = ['state', 'city']
    search_fields = ['street', 'city', 'user__name']

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'region', 'status']
    list_filter = ['type', 'region', 'status']
    search_fields = ['name', 'type']

@admin.register(ComponentType)
class ComponentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'table_name', 'description']

@admin.register(Reservoir)
class ReservoirAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'capacity', 'plant', 'status']
    list_filter = ['type', 'status']

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'serial_number', 'status']
    list_filter = ['type', 'status']
    search_fields = ['name', 'serial_number']