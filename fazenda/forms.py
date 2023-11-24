from .models import Cliente, Produto
from django.forms import ModelForm


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "empresa", "telefone"]


class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "tempo_preparo"]
