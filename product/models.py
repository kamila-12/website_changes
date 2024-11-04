from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    address = models.CharField(max_length=255)
    trade_for = models.CharField(max_length=255)
    #owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    
    def __str__(self):
        return self.title

    
class Exchanged(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    product_offered = models.ForeignKey(Product, related_name='exchanges_offered', on_delete=models.CASCADE)
    product_requested = models.ForeignKey(Product, related_name='exchanges_requested', on_delete=models.CASCADE)
    user_requested = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exchange {self.id} - {self.status}"