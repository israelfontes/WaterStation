from django import forms
from apps.users.models import Address
from .models import Region, Plant, Sensor, WaterWell, Dissalinator, Reservoir

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'number', 'neighborhood', 'city', 'state', 'cep', 'latitude', 'longitude']
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua/Avenida'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Latitude', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Longitude', 'step': 'any'}),
        }

class WaterWellForm(forms.ModelForm):
    class Meta:
        model = WaterWell
        fields = ['name', 'depth', 'sensors']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Poço'}),
            'depth': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Profundidade (m)', 'step': 'any'}),
            'sensors': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

class DissalinatorForm(forms.ModelForm):
    class Meta:
        model = Dissalinator
        fields = ['name', 'capacity', 'sensors']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Dessalinizador'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidade (L/h)', 'step': 'any'}),
            'sensors': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

class ReservoirForm(forms.ModelForm):
    class Meta:
        model = Reservoir
        fields = ['name', 'capacity', 'sensors']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Reservatório'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidade (L)', 'step': 'any'}),
            'sensors': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'plant_type', 'region', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Planta'}),
            'plant_type': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PlantCompleteForm:
    """
    Classe para gerenciar múltiplos formulários da planta
    """
    def __init__(self, data=None):
        self.address_form = AddressForm(data, prefix='address')
        self.plant_form = PlantForm(data, prefix='plant')
        self.water_well_form = WaterWellForm(data, prefix='water_well')
        self.dissalinator_form = DissalinatorForm(data, prefix='dissalinator')
        self.reservoir_form = ReservoirForm(data, prefix='reservoir')
    
    def is_valid(self):
        return (self.address_form.is_valid() and 
                self.plant_form.is_valid() and 
                self.water_well_form.is_valid() and 
                self.dissalinator_form.is_valid() and 
                self.reservoir_form.is_valid())
    
    def save(self):
        # Salvar endereço
        address = self.address_form.save()
        
        # Salvar componentes
        water_well = self.water_well_form.save()
        dissalinator = self.dissalinator_form.save()
        reservoir = self.reservoir_form.save()
        
        # Salvar planta
        plant = self.plant_form.save(commit=False)
        plant.address = address
        plant.water_well = water_well
        plant.dissalinator = dissalinator
        plant.reservoir = reservoir
        plant.save()
        
        return plant