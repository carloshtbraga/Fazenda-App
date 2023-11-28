from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Sum, F, Q, Count, ExpressionWrapper, DecimalField
from .forms import ClienteForm, PedidoForm, ProdutoForm, ItemPedidoForm
from .models import Cliente, Pedido, Produto, ItemPedido
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    return render(request, "index.html")


def listar_clientes(request):
    termo_pesquisa = request.GET.get("q")

    if termo_pesquisa:
        clientes = Cliente.objects.filter(
            Q(nome__icontains=termo_pesquisa) | Q(empresa__icontains=termo_pesquisa)
        ).order_by(
            "nome"
        )  # Ordena por nome (ou qualquer campo desejado)
    else:
        clientes = Cliente.objects.all().order_by(
            "nome"
        )  # Ordena por nome (ou qualquer campo desejado)

    paginator = Paginator(clientes, 5)  # Define 5 itens por página
    page_number = request.GET.get("page")

    try:
        clientes_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        clientes_paginados = paginator.page(1)
    except EmptyPage:
        clientes_paginados = paginator.page(paginator.num_pages)

    return render(
        request,
        "listar_clientes.html",
        {"clientes": clientes_paginados},
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
    termo_pesquisa = request.GET.get("q")
    produtos = Produto.objects.all()

    if termo_pesquisa:
        produtos = produtos.filter(nome__icontains=termo_pesquisa)

    produtos_com_total = produtos.annotate(
        total_produto=Sum("itempedido__quantidade")
    ).order_by("nome")

    paginator = Paginator(produtos_com_total, 5)  # Define 5 itens por página
    page_number = request.GET.get("page")

    try:
        produtos_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        produtos_paginados = paginator.page(1)
    except EmptyPage:
        produtos_paginados = paginator.page(paginator.num_pages)

    total_produtos = produtos_com_total.count()

    return render(
        request,
        "listar_produtos.html",
        {"produtos": produtos_paginados, "total_produtos": total_produtos},
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
            | Q(
                pk__icontains=termo_pesquisa
            )  # Procurar pelo ID do pedido (chave primária)
        )

    return render(request, "listar_pedidos.html", {"pedidos": pedidos})


def listar_pedidos_concluidos(request):
    termo_pesquisa = request.GET.get("q")

    pedidos = Pedido.objects.filter(status="Concluído").order_by("pk")

    if termo_pesquisa:
        pedidos = pedidos.filter(
            Q(cliente__nome__icontains=termo_pesquisa)
            | Q(cliente__empresa__icontains=termo_pesquisa)
            | Q(pk__icontains=termo_pesquisa)
        )

    paginator = Paginator(pedidos, 5)  # Define 5 itens por página
    page_number = request.GET.get("page")

    try:
        pedidos_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        pedidos_paginados = paginator.page(1)
    except EmptyPage:
        pedidos_paginados = paginator.page(paginator.num_pages)

    return render(
        request,
        "listar_pedidos_concluidos.html",
        {"pedidos": pedidos_paginados},
    )


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


def estatisticas(request):
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")

    pedidos_pendentes = Pedido.objects.filter(status="Pendente")

    valor_pedidos_pendentes = 0

    for pedido in pedidos_pendentes:
        itens_pedido = pedido.itempedido_set.all()
        valor_pedido = sum(item.quantidade * item.preco for item in itens_pedido)
        valor_pedidos_pendentes += valor_pedido

    valor_pedidos_concluidos = 0
    total_pedidos_mes_atual = 0
    pedidos_no_periodo = []

    if data_inicio and data_fim:
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()

        pedidos_concluidos = Pedido.objects.filter(
            status="Concluído", data_pedido__range=(data_inicio, data_fim)
        )

        valor_pedidos_concluidos = (
            pedidos_concluidos.aggregate(
                total=ExpressionWrapper(
                    Sum(F("itempedido__quantidade") * F("itempedido__preco")),
                    output_field=DecimalField(),
                )
            )["total"]
            or 0
        )

        total_pedidos_mes_atual = pedidos_concluidos.count()

        pedidos_no_periodo = pedidos_concluidos.values_list(
            "id", "cliente__nome", "cliente__empresa"
        )

    return render(
        request,
        "estatisticas.html",
        {
            "valor_pedidos_concluidos": valor_pedidos_concluidos,
            "valor_pedidos_pendentes": valor_pedidos_pendentes,
            "total_pedidos_mes_atual": total_pedidos_mes_atual,
            "pedidos_no_periodo": pedidos_no_periodo,
        },
    )
