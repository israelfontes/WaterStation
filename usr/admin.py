from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import UserRegion, Address, Plant, ComponentType, Reservoir, Sensor

Users = get_user_model()

class UserRegionInline(admin.TabularInline):
    model = UserRegion
    extra = 1

@admin.register(Users)
class UsersAdmin(BaseUserAdmin):
    # Exibir colunas: username, email, status, is_staff, is_superuser
    list_display = ['username', 'email', 'status', 'is_staff', 'is_superuser']
    list_filter = ['status', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email']
    ordering = ['username']
    inlines = [UserRegionInline]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('email',)}),
        ('Status e Permissões', {'fields': ('status', 'is_active', 'is_staff', 'is_superuser')}),
        ('Grupos e Permissões Específicas', {'fields': ('groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'street', 'city', 'state', 'user']
    list_filter = ['state', 'city']
    search_fields = ['street', 'city', 'user__username']

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