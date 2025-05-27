from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Address, ComponentType, Sensor

Users = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Senha'
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label='Nível de Autorização',
        required=True,
        help_text='Selecione o nível de acesso do usuário.'
    )

    class Meta:
        model = Users
        fields = ['username', 'password', 'status', 'group']
        labels = {
            'username': 'Nome de Usuário',
            'status': 'Status'
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'number', 'neighborhood', 'city', 'state', 'cep', 'coordinates']
        labels = {
            'street': 'Rua',
            'number': 'Número',
            'neighborhood': 'Bairro',
            'city': 'Cidade',
            'state': 'Estado',
            'cep': 'CEP',
            'coordinates': 'Coordenadas'
        }

class ComponentForm(forms.ModelForm):
    class Meta:
        model = ComponentType
        fields = ['name', 'table_name', 'description']
        labels = {
            'name': 'Nome do Componente',
            'table_name': 'Nome da Tabela',
            'description': 'Descrição'
        }

class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ['type', 'name', 'model', 'serial_number', 'status']
        labels = {
            'type': 'Tipo do Sensor',
            'name': 'Nome do Sensor',
            'model': 'Modelo',
            'serial_number': 'Número de Série',
            'status': 'Status'
        }
