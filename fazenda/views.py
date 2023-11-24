from django.shortcuts import render, redirect
from .models import Cliente, Produto
from .forms import ClienteForm, ProdutoForm


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
