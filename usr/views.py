from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView as DjangoLogoutView

from .decorators import any_group_required
from .forms import UserForm, AddressForm, ComponentForm, SensorForm
from django.contrib.auth.hashers import make_password

class LogoutView(DjangoLogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# Login padrão
def login_view(request):
    if request.user.is_authenticated:
        return redirect('usr:home')
    
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('usr:home')
    return render(request, 'usr/login.html', {'form': form})

# Logout via GET redirecionado para POST
logout_view = LogoutView.as_view(next_page='usr:login')

@login_required
def home_view(request):
    return render(request, 'usr/home.html')

# Cadastrar Usuário e Endereço juntos
@any_group_required('ADMIN', 'OPERATOR')
def cadastrar_usuario(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        address_form = AddressForm(request.POST)
        if user_form.is_valid() and address_form.is_valid():
            # Cria usuário sem salvar e define senha criptografada
            u = user_form.save(commit=False)
            u.password = make_password(user_form.cleaned_data['password'])
            u.save()
            # Associa grupo (nível de autorização)
            grupo = user_form.cleaned_data['group']
            u.groups.set([grupo])

            # Cria endereço e associa ao usuário
            endereco = address_form.save(commit=False)
            endereco.user = u
            endereco.save()

            messages.success(request, 'Usuário e endereço cadastrados com sucesso.')
            return redirect('usr:home')
    else:
        user_form = UserForm()
        address_form = AddressForm()
    return render(request, 'usr/cadastrar_usuario.html', {
        'user_form': user_form,
        'address_form': address_form,
    })

# Cadastrar Componente e Sensor juntos
@any_group_required('ADMIN', 'OPERATOR')
def cadastrar_componente(request):
    if request.method == 'POST':
        comp_form = ComponentForm(request.POST)
        sensor_form = SensorForm(request.POST)
        if comp_form.is_valid() and sensor_form.is_valid():
            comp = comp_form.save()
            sensor = sensor_form.save(commit=False)
            sensor.component = comp
            sensor.save()

            messages.success(request, 'Componente e sensor cadastrados com sucesso.')
            return redirect('usr:home')
    else:
        comp_form = ComponentForm()
        sensor_form = SensorForm()
    return render(request, 'usr/cadastrar_componente.html', {
        'comp_form': comp_form,
        'sensor_form': sensor_form,
    })
