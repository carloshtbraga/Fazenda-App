from .models import Cliente, Produto, Pedido, ItemPedido
from django.forms import ModelForm
from django import forms


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "empresa", "telefone"]


class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "tempo_preparo"]


class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        exclude = ["produtos"]


class ItemPedidoForm(ModelForm):
    class Meta:
        model = ItemPedido
        fields = ["produto", "quantidade", "preco"]
