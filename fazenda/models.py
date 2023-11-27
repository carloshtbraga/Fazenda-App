from django.db import models
from datetime import timedelta


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    tempo_preparo = models.PositiveIntegerField()

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through="ItemPedido")
    data_pedido = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=(
            ("Pendente", "Pendente"),
            ("Concluído", "Concluído"),
        ),
        default="Pendente",
    )

    def maior_tempo_preparo(self):
        tempos_preparo = self.produtos.all().values_list("tempo_preparo", flat=True)
        if tempos_preparo:
            return max(tempos_preparo)
        return 0

    def data_entrega(self):
        maior_tempo = self.maior_tempo_preparo()
        if maior_tempo > 0:
            return self.data_pedido + timedelta(days=maior_tempo)
        return self.data_pedido

    def __str__(self):
        itens = ", ".join(
            [
                f"{item.quantidade}x {item.produto.nome} por R$ {item.preco}"
                for item in self.itempedido_set.all()
            ]
        )
        return f"Pedido de {self.cliente} em {self.data_pedido} com {itens}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    marcado = models.BooleanField(default=False)  
    
    def data_entrega_produto(self):
        data_pedido = self.pedido.data_pedido
        tempo_preparo_produto = self.produto.tempo_preparo
        if data_pedido and tempo_preparo_produto:
            return data_pedido + timedelta(days=tempo_preparo_produto)
        return None

    def __str__(self):
        return f"{self.quantidade}x {self.produto} por R$ {self.preco } no pedido {self.pedido.pk}"
