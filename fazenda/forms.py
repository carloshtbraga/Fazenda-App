from .models import Cliente, Produto, Pedido, ItemPedido
from django.forms import ModelForm
from django import forms


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "empresa", "telefone"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "empresa": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
        }


class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "tempo_preparo"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "tempo_preparo": forms.NumberInput(attrs={"class": "form-control"}),
        }


class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        exclude = ["produtos", "status"]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)
        self.fields["cliente"].empty_label = "Selecione o Cliente"


class ItemPedidoForm(ModelForm):
    class Meta:
        model = ItemPedido
        fields = ["produto", "quantidade", "preco"]
        widgets = {
            "produto": forms.Select(attrs={"class": "form-control"}),
            "quantidade": forms.NumberInput(attrs={"class": "form-control"}),
            "preco": forms.NumberInput(attrs={"class": "form-control"}),
        }
