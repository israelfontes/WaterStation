from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('usr:home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('usr:home')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'usr/login.html', {'form': form})

@login_required
def home_view(request):
    # Verificar se é admin
    if not request.user.is_superuser:
        messages.error(request, 'Acesso negado. Apenas administradores.')
        return redirect('usr:login')
    
    return render(request, 'usr/home.html')

@login_required
def cadastrar_usuario(request):
    # Implementar depois
    return render(request, 'usr/cadastrar_usuario.html')

@login_required
def cadastrar_endereco(request):
    # Implementar depois
    return render(request, 'usr/cadastrar_endereco.html')

@login_required
def cadastrar_componente(request):
    # Implementar depois
    return render(request, 'usr/cadastrar_componente.html')

@login_required
def instalar_sensor(request):
    # Implementar depois
    return render(request, 'usr/instalar_sensor.html')