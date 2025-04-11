from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, logout
from django.http import JsonResponse
from django.db.models import Q
from products.models import ProductCategory, Product, Basket, OrderItem
from products.forms import LoginForm, RegisterForm, ProfileForm, OrderForm

def index(request):
    return render(request, 'products/index.html')

def products(request):
    context = {
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)

def products_by_category(request, category_id):
    category = ProductCategory.objects.get(id=category_id)
    products = Product.objects.filter(category=category)

    context = {
        'products': products,
        'categories': ProductCategory.objects.all(),
        'selected_category': category
    }
    return render(request, 'products/products.html', context)

def contact(request):
    return render(request, 'products/contact.html')

def delivery(request):
    return render(request, 'products/delivery.html')

def about(request):
    return render(request, 'products/about.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'products/product_detail.html', {'product': product, 'related_products': related_products})

def search_products(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        products = Product.objects.filter(Q(name__icontains=query) )[:5]
        for product in products:
            results.append({
                'name': product.name,
                'price': str(product.price),
                'url': f'/products/{product.id}/',
            })
    return JsonResponse({'results': results})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index') 
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth/signup.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Зміни збережено.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'user/profile.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('login')
    
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'products'))

@login_required
def basket_view(request):
    baskets = Basket.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in baskets)

    return render(request, 'products/basket.html', {
        'baskets': baskets,
        'total_price': total_price,
    })

@login_required
def basket_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    basket_item = Basket.objects.filter(user=request.user, product=product).first()
    if basket_item:
        basket_item.delete()
    return redirect("basket")

@login_required
def checkout(request):
    baskets = Basket.objects.filter(user=request.user)
    if not baskets.exists():
        return redirect('products')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for basket in baskets:
                OrderItem.objects.create(
                    order=order,
                    product=basket.product,
                    quantity=basket.quantity,
                    price=basket.product.price
                )
            baskets.delete()
            return redirect('index')
    else:
        form = OrderForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        })

    total_price = sum(item.product.price * item.quantity for item in baskets)

    return render(request, 'products/checkout.html', {
        'form': form,
        'baskets': baskets,
        'total_price': total_price
    })