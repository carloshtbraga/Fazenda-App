from django.shortcuts import render, redirect
from .models import Cliente
from .forms import ClienteForm


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
