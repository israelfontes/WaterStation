from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view, home_view, cadastrar_usuario, cadastrar_componente

app_name = 'usr'

urlpatterns = [
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', home_view, name='home'),
    path('cadastrar-usuario/', cadastrar_usuario, name='cadastrar_usuario'),
    path('cadastrar-componente/', cadastrar_componente, name='cadastrar_componente'),
]