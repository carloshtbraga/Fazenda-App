from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path('', views.listar_clientes, name='listar_clientes'),
    path('clientes/novo/', views.criar_cliente, name='criar_cliente'),
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('produtos/novo/', views.criar_produto, name='criar_produto'),
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('pedidos/novo/', views.criar_pedido, name='criar_pedido'),
    path('item_pedido/<int:pk>/', views.detalhes_item_pedido, name='detalhes_item_pedido'),
    path('pedido/<int:pedido_id>/adicionar_item/', views.adicionar_item_pedido, name='adicionar_item_pedido'),
]

