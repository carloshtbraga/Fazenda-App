from django.db import models


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

    def __str__(self):
        itens = ', '.join([f"{item.quantidade}x {item.produto.nome} por R$ {item.preco}" for item in self.itempedido_set.all()])
        return f"Pedido de {self.cliente} em {self.data_pedido} com {itens}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    # Adicione outros campos relevantes para o item do pedido, se necessário

    def __str__(self):
        return f"{self.quantidade}x {self.produto} por R$ {self.preco } no pedido {self.pedido.pk}"
