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
        fields = ['name', 'depth', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Poço'}),
            'depth': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Profundidade (m)', 'step': 'any'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class DissalinatorForm(forms.ModelForm):
    class Meta:
        model = Dissalinator
        fields = ['name', 'capacity', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Dessalinizador'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidade (L/h)', 'step': 'any'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ReservoirForm(forms.ModelForm):
    class Meta:
        model = Reservoir
        fields = ['name', 'capacity', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Reservatório'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidade (L)', 'step': 'any'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
    def __init__(self, data=None, instance=None):
        # Se editando uma planta existente
        if instance:
            self.plant_form = PlantForm(data, prefix='plant', instance=instance)
            self.address_form = AddressForm(data, prefix='address', instance=instance.address)
            self.water_well_form = WaterWellForm(data, prefix='water_well', instance=instance.water_well)
            self.dissalinator_form = DissalinatorForm(data, prefix='dissalinator', instance=instance.dissalinator)
            self.reservoir_form = ReservoirForm(data, prefix='reservoir', instance=instance.reservoir)
        else:
            # Criando nova planta
            self.plant_form = PlantForm(data, prefix='plant')
            self.address_form = AddressForm(data, prefix='address')
            self.water_well_form = WaterWellForm(data, prefix='water_well')
            self.dissalinator_form = DissalinatorForm(data, prefix='dissalinator')
            self.reservoir_form = ReservoirForm(data, prefix='reservoir')
        
        self.instance = instance
    
    def is_valid(self):
        return (self.address_form.is_valid() and 
                self.plant_form.is_valid() and 
                self.water_well_form.is_valid() and 
                self.dissalinator_form.is_valid() and 
                self.reservoir_form.is_valid())
    
    def save(self):
        if self.instance:
            # Atualizando planta existente
            address = self.address_form.save()
            water_well = self.water_well_form.save()
            dissalinator = self.dissalinator_form.save()
            reservoir = self.reservoir_form.save()
            
            plant = self.plant_form.save(commit=False)
            plant.address = address
            plant.water_well = water_well
            plant.dissalinator = dissalinator
            plant.reservoir = reservoir
            plant.save()
            
            return plant
        else:
            # Criando nova planta
            address = self.address_form.save()
            water_well = self.water_well_form.save()
            dissalinator = self.dissalinator_form.save()
            reservoir = self.reservoir_form.save()
            
            plant = self.plant_form.save(commit=False)
            plant.address = address
            plant.water_well = water_well
            plant.dissalinator = dissalinator
            plant.reservoir = reservoir
            plant.save()
            
            return plant

# Formulário simples para criação rápida
class PlantSimpleForm(forms.Form):
    plant_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Planta'})
    )
    plant_type = forms.ChoiceField(
        choices=Plant.PLANT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Campos de endereço
    street = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua'})
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'})
    )
    state = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'})
    )
    
    def save(self):
        """Salvar usando dados do formulário simples"""
        from apps.users.models import Address
        
        # Criar endereço básico
        address = Address.objects.create(
            street=self.cleaned_data['street'],
            number='S/N',
            neighborhood='Centro',
            city=self.cleaned_data['city'],
            state=self.cleaned_data['state'],
            cep='00000-000'
        )
        
        # Criar componentes básicos
        water_well = WaterWell.objects.create(
            name=f"Poço {self.cleaned_data['plant_name']}",
            depth=100.00
        )
        
        dissalinator = Dissalinator.objects.create(
            name=f"Dessalinizador {self.cleaned_data['plant_name']}",
            capacity=500.00
        )
        
        reservoir = Reservoir.objects.create(
            name=f"Reservatório {self.cleaned_data['plant_name']}",
            capacity=10000.00
        )
        
        # Criar planta
        plant = Plant.objects.create(
            name=self.cleaned_data['plant_name'],
            plant_type=self.cleaned_data['plant_type'],
            address=address,
            region=self.cleaned_data['region'],
            water_well=water_well,
            dissalinator=dissalinator,
            reservoir=reservoir
        )
        
        return plant