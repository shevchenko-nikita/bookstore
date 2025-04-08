from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from products.models import ProductCategory, Product
from products.forms import LoginForm, RegisterForm

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