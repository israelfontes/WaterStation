from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usr'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home_view, name='home'),
    path('cadastrar-usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('cadastrar-endereco/', views.cadastrar_endereco, name='cadastrar_endereco'),
    path('cadastrar-componente/', views.cadastrar_componente, name='cadastrar_componente'),
    path('instalar-sensor/', views.instalar_sensor, name='instalar_sensor'),
]