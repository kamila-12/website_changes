from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    address = models.CharField(max_length=255)
    trade_for = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title

    