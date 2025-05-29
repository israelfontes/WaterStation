# apps/monitoring/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Listagem de plantas
    path('plants/', views.plant_list, name='plant_list'),
    
    # CRUD de plantas
    path('plants/create/', views.plant_create, name='plant_create'),
    path('plants/<int:pk>/', views.plant_detail, name='plant_detail'),
    path('plants/<int:pk>/edit/', views.plant_edit, name='plant_edit'),
    path('plants/<int:pk>/delete/', views.plant_delete, name='plant_delete'),
    path('plants/<int:pk>/toggle-status/', views.plant_toggle_status, name='plant_toggle_status'),
]