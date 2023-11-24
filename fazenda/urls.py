from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/novo/', views.criar_cliente, name='criar_cliente'),
]
