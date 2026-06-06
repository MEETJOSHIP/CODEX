from django.db import models
from django.utils import timezone
from datetime import timedelta
from procurement.models import PurchaseOrder
from vendors.models import Vendor

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    purchase_order = models.OneToOneField(PurchaseOrder, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    issued_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            count = Invoice.objects.count() + 1
            self.invoice_number = f"INV-{count:05d}"
            
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=30)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number