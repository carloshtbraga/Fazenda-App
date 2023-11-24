from django.shortcuts import render, redirect
from .models import Cliente, Produto, Pedido
from .forms import ClienteForm, ProdutoForm, PedidoForm, ItemPedidoForm


# Create your views here.
def index(request):
    return render(request, "index.html")


def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "listar_clientes.html", {"clientes": clientes})


def criar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_clientes")
    else:
        form = ClienteForm()
    return render(request, "criar_cliente.html", {"form": form})


def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, "listar_produtos.html", {"produtos": produtos})


def criar_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_produtos")
    else:
        form = ProdutoForm()
    return render(request, "criar_produto.html", {"form": form})


def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, "listar_pedidos.html", {"pedidos": pedidos})


def criar_pedido(request):
    if request.method == "POST":
        pedido_form = PedidoForm(request.POST)
        item_pedido_formset = ItemPedidoForm(request.POST)

        if pedido_form.is_valid() and item_pedido_formset.is_valid():
            pedido = pedido_form.save()
            itens_pedido = item_pedido_formset.save(commit=False)

            for item in itens_pedido:
                item.pedido = pedido
                item.save()

            return redirect("listar_pedidos")
    else:
        pedido_form = PedidoForm()
        item_pedido_formset = ItemPedidoForm()

    return render(
        request,
        "criar_pedido.html",
        {"pedido_form": pedido_form, "item_pedido_formset": item_pedido_formset},
    )
