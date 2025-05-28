from django.urls import path
from . import views

urlpatterns = [
    path('plants/', views.plant_list, name='plant_list'),
    path('plants/create/', views.plant_create, name='plant_create'),
    path('plants/<int:pk>/', views.plant_detail, name='plant_detail'),
]