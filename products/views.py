from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, logout

from products.models import ProductCategory, Product
from products.forms import LoginForm, RegisterForm, ProfileForm

def index(request):
    return render(request, 'products/index.html')

def products(request):
    context = {
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)

def delivery(request):
    return render(request, 'products/delivery.html')

def about(request):
    return render(request, 'products/about.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'products/product_detail.html', {'product': product, 'related_products': related_products})

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