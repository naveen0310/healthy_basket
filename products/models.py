from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='frontend/templates/static/', blank=True, null=True)
    # Add other fields as needed

    def __str__(self):
        return self.name
