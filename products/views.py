from django.shortcuts import render

def index(request):
    return render(request, 'products/index.html')

def products(request):
    context = {
        'image_url': 'static/images/book1.jpg',
        'title': 'first book',
        'description': 'test text for description la la la',
        'price': 200,
    }
    return render(request, 'products/products.html', context)