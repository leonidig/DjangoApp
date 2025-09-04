from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from django.contrib import messages

from .forms import ProductForm
from .models import Product, Category



def index(request):
    products = Product.objects.all()

    title = request.GET.get("title")
    category_id = request.GET.get("category")
    sort_price = request.GET.get("sort_price")

    if title:
        products = products.filter(name__icontains=title)

    if category_id:
        products = products.filter(category_id=category_id)

    if sort_price == "desc":
        products = products.order_by("-price")
    elif sort_price == "asc":
        products = products.order_by("price")

    categories = Category.objects.all()

    return render(request, "index.html", {
        "products": products,
        "categories": categories
    })



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


def product_detail(request, id: int):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'product_detail.html', {'product': product})



def delete_product(request, id: int):
    product = get_object_or_404(Product, pk=id)

    if request.user != product.owner:
        return HttpResponseForbidden("You are not allowed to delete this product.")

    messages.success(request, f'Product `{product.name}` was deleted successfully!')
    product.delete()
    return redirect('products:index')


def update_product(request, id: int):
    product = get_object_or_404(Product, pk=id)

    if request.user != product.owner:
        return HttpResponseForbidden("You are not allowed to edit this product.")

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product `{product.name}` was updated successfully!')
            return redirect('products:index')
    else:
        form = ProductForm(instance=product)
    return render(request, 'update_product.html', {'form': form, 'product': product})