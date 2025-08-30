from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .forms import ProductForm



def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:login')

    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)  # поки не зберігаємо
            product.owner = request.user       # прив’язуємо власника
            product.save()                     # тепер зберігаємо
            return redirect("products:index")  # редірект після створення
    else:
        form = ProductForm()

    return render(request, "create_product.html", {"form": form})