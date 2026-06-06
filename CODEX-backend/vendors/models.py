from django.db import models

class Vendor(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
    ]

    name = models.CharField(max_length=255)

    gst_number = models.CharField(
        max_length=50,
        unique=True
    )

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    category = models.CharField(max_length=100)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    address = models.TextField(blank=True)
    
    country = models.CharField(max_length=100, default='India')
    
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    created_at = models.DateTimeField(
        auto_now_add=True
    )