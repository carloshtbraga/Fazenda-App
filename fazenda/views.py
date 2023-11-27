from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Sum, F, Q
from .forms import ClienteForm, PedidoForm, ProdutoForm, ItemPedidoForm
from .models import Cliente, Pedido, Produto, ItemPedido


# Create your views here.
def index(request):
    return render(request, "index.html")


def listar_clientes(request):
    termo_pesquisa = request.GET.get("q")  # Obtém o termo de pesquisa, se presente
    if termo_pesquisa:
        clientes = Cliente.objects.filter(
            Q(nome__icontains=termo_pesquisa) | Q(empresa__icontains=termo_pesquisa)
        )
    else:
        clientes = Cliente.objects.all()

    total_clientes = clientes.count()  # Obtém o total de clientes

    return render(
        request,
        "listar_clientes.html",
        {"clientes": clientes, "total_clientes": total_clientes},
    )


def criar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_clientes")
    else:
        form = ClienteForm()
    return render(request, "criar_cliente.html", {"form": form})


def atualizar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("listar_clientes")
    else:
        form = ClienteForm(instance=cliente)

    return render(request, "atualizar_cliente.html", {"form": form})


def deletar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return redirect("listar_clientes")

    return render(request, "deletar_cliente.html", {"cliente": cliente})


def listar_produtos(request):
    termo_pesquisa = request.GET.get("q")  # Obtém o termo de pesquisa, se presente
    if termo_pesquisa:
        produtos = Produto.objects.filter(nome__icontains=termo_pesquisa)
    else:
        produtos = Produto.objects.all()

    total_produtos = produtos.count()  # Obtém o total de produtos

    return render(
        request,
        "listar_produtos.html",
        {"produtos": produtos, "total_produtos": total_produtos},
    )


def criar_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_produtos")
    else:
        form = ProdutoForm()
    return render(request, "criar_produto.html", {"form": form})


def atualizar_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect("listar_produtos")
    else:
        form = ProdutoForm(instance=produto)
    return render(request, "atualizar_produto.html", {"form": form, "produto": produto})


def deletar_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)

    if request.method == "POST":
        produto.delete()
        return redirect("listar_produtos")

    return render(request, "deletar_produto.html", {"produto": produto})


def listar_pedidos(request):
    termo_pesquisa = request.GET.get("q")

    pedidos = Pedido.objects.filter(status="Pendente")

    if termo_pesquisa:
        pedidos = pedidos.filter(
            Q(cliente__nome__icontains=termo_pesquisa)
            | Q(cliente__empresa__icontains=termo_pesquisa)
        )

    return render(request, "listar_pedidos.html", {"pedidos": pedidos})


def listar_pedidos_concluidos(request):
    termo_pesquisa = request.GET.get("q")

    pedidos = Pedido.objects.filter(status="Concluído")

    if termo_pesquisa:
        pedidos = pedidos.filter(
            Q(cliente__nome__icontains=termo_pesquisa)
            | Q(cliente__empresa__icontains=termo_pesquisa)
        )

    return render(request, "listar_pedidos_concluidos.html", {"pedidos": pedidos})


def criar_pedido(request):
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            print("FORMROFMROM", form)
            id = form.save()
            return redirect(
                "detalhes_item_pedido", pk=id.id
            )  # Redireciona para a lista de pedidos após a criação bem-sucedida
    else:
        form = PedidoForm()

    return render(request, "criar_pedido.html", {"form": form})


def deletar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    if request.method == "POST":
        pedido.delete()
        return redirect("listar_pedidos")
    return render(request, "deletar_pedido.html", {"pedido": pedido})


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
            return redirect("detalhes_item_pedido", pk=pedido_id)
    else:
        form = ItemPedidoForm()

    return render(request, "adicionar_item_pedido.html", {"form": form})


def marcar_pedido_como_concluido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    if pedido.status == "Pendente":
        pedido.status = "Concluído"
    else:
        pedido.status = "Pendente"
    pedido.save()
    return redirect("detalhes_item_pedido", pk=pedido_id)


def alternar_checkbox_item_pedido(request, item_pedido_id):
    item_pedido = get_object_or_404(ItemPedido, pk=item_pedido_id)
    item_pedido.marcado = not item_pedido.marcado
    item_pedido.save()
    return print("foi")
