from django.contrib import admin
from .models import Cliente, Produto, Pedido, ItemPedido


admin.site.register(Cliente)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
