from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Sum, F
from .forms import ClienteForm, PedidoForm, ProdutoForm, ItemPedidoForm
from .models import Cliente, Pedido, Produto, ItemPedido


# Create your views here.
def index(request):
    return render(request, "index.html")


def listar_clientes(request):
    clientes = Cliente.objects.all()  # type: ignore
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
    produtos = Produto.objects.all()  # type: ignore
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
    pedidos = Pedido.objects.annotate(
        total_pedido=Sum(F("itempedido__quantidade") * F("itempedido__preco"))
    )
    return render(request, "listar_pedidos.html", {"pedidos": pedidos})


def criar_pedido(request):
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "listar_pedidos"
            )  # Redireciona para a lista de pedidos após a criação bem-sucedida
    else:
        form = PedidoForm()

    return render(request, "criar_pedido.html", {"form": form})


def detalhes_item_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    pedido.total_pedido = (
        pedido.itempedido_set.aggregate(total=Sum(F("quantidade") * F("preco")))[
            "total"
        ]
        or 0
    )  # Caso não haja itens no pedido

    return render(request, "detalhes_item_pedido.html", {"pedido": pedido})


def adicionar_item_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    if request.method == "POST":
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False)
            item_pedido.pedido = pedido
            item_pedido.save()
            return redirect("listar_pedidos")
    else:
        form = ItemPedidoForm()

    return render(request, "adicionar_item_pedido.html", {"form": form})


def pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, "pedido.html", {"pedido": pedido})
