from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.listar_clientes, name="listar_clientes"),
    path("clientes/novo/", views.criar_cliente, name="criar_cliente"),
    path(
        "clientes/atualizar/<int:pk>/",
        views.atualizar_cliente,
        name="atualizar_cliente",
    ),
    path("clientes/deletar/<int:pk>/", views.deletar_cliente, name="deletar_cliente"),
    path("produtos/", views.listar_produtos, name="listar_produtos"),
    path(
        "produtos/<int:produto_id>/atualizar/",
        views.atualizar_produto,
        name="atualizar_produto",
    ),
    path(
        "produtos/<int:produto_id>/deletar/",
        views.deletar_produto,
        name="deletar_produto",
    ),
    path("produtos/novo/", views.criar_produto, name="criar_produto"),
    path("pedidos/", views.listar_pedidos, name="listar_pedidos"),
    path("pedidos/novo/", views.criar_pedido, name="criar_pedido"),
    path(
        "pedido/<int:pedido_id>/adicionar_item/",
        views.adicionar_item_pedido,
        name="adicionar_item_pedido",
    ),
    path(
        "pedidos/<int:pedido_id>/deletar/", views.deletar_pedido, name="deletar_pedido"
    ),
    path(
        "pedido/<int:pedido_id>/concluir/",
        views.marcar_pedido_como_concluido,
        name="concluir_pedido",
    ),
    path(
        "detalhes_item_pedido/<int:pk>/",
        views.detalhes_item_pedido,
        name="detalhes_item_pedido",
    ),
    path(
        "alternar-checkbox/<int:item_pedido_id>/",
        views.alternar_checkbox_item_pedido,
        name="alternar_checkbox_item_pedido",
    ),
]
