from django.db import models
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length = 128)
    description = models.TextField(null = True, blank = True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 256)
    author_name = models.CharField(max_length = 256, null = True)
    description = models.TextField()
    price = models.DecimalField(max_digits = 6, decimal_places = 2)
    quantity = models.PositiveIntegerField(default = 0)
    image = models.ImageField(upload_to = 'products_images')
    category = models.ForeignKey(to = ProductCategory, on_delete = models.CASCADE)

    def __str__(self):
        return f'Книга: { self.name } | Категорія: {self.category.name}'
    
class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity=models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для #{self.user.username} | продукт: #{self.product.name}'


class Order(models.Model):
    PAYMENT_METHODS = [
        ('card', 'Картка'),
        ('cash', 'Готівка при отриманні'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=256)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Замовлення #{self.id} від {self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"