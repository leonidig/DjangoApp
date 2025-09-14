from collections import defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from django.contrib import messages

from .forms import ProductForm, CartAddForm
from .models import Product, Category, Cart, CartItem, Order, OrderItem


@login_required
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
    new_orders = OrderItem.objects.filter(product__owner=request.user, order__status="pending").exists()

    return render(request, "index.html", {
        "products": products,
        "categories": categories,
        "new_orders": new_orders
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


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart/detail.html", {"cart": cart})


@login_required
def cart_add(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
    return redirect("products:cart_detail")

@login_required
def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("products:cart_detail")


@login_required
def cart_update(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "increase":
            item.quantity += 1
            item.save()
        elif action == "decrease":
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
        else:
            quantity = int(request.POST.get("quantity", 1))
            if quantity > 0:
                item.quantity = quantity
                item.save()
            else:
                item.delete()
    return redirect("products:cart_detail")


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        return redirect("products:cart_detail")

    items_by_owner = defaultdict(list)
    for item in cart.items.all():
        items_by_owner[item.product.owner].append(item)

    created_orders = []

    for owner, items in items_by_owner.items():
        order = Order.objects.create(user=request.user)
        for cart_item in items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )
        created_orders.append(order)

    cart.items.all().delete()

    return redirect("products:order_detail", order_id=created_orders[0].id)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/detail.html", {"order": order})


@login_required
def seller_orders(request):
    orders = Order.objects.filter(items__product__owner=request.user).distinct()

    return render(request, "orders/seller_orders.html", {"orders": orders})


@login_required
def seller_confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, items__product__owner=request.user)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "accept":
            order.status = "processing"
            order.save()
        elif action == "reject":
            order.status = "canceled"
            order.save()
        return redirect("products:seller_orders")

    seller_items = order.items.filter(product__owner=request.user)
    return render(request, "orders/seller_order_detail.html", {"order": order, "items": seller_items})



@login_required
def my_orders(request):
    orders = request.user.orders.all().order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": orders})