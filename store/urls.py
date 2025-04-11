"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from products.views import index, products, delivery, about, product_detail, products_by_category
from products.views import login_view, signup_view, profile_view, delete_account, logout_view
from products.views import search_products


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('products', products, name='products'),
    path('products/category/<int:category_id>/', products_by_category, name='products_by_category'),
    path('delivery', delivery, name='delivery'),
    path('about', about, name='about'),
    path('profile', profile_view, name='profile'),
    path('delete_account', delete_account, name='delete_account'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),

    path('search/', search_products, name='search_products'),

    path('login', login_view, name='login'),
    path('signup', signup_view, name='signup'),
    path('logout', logout_view, name='logout')
]

if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)