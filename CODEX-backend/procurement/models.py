from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from vendors.models import Vendor

class RFQ(models.Model):
    RFQ_STATUS = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.PositiveIntegerField(null=True, blank=True)
    deadline = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vendors = models.ManyToManyField(Vendor)
    status = models.CharField(max_length=20, choices=RFQ_STATUS, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class RFQItem(models.Model):
    rfq = models.ForeignKey(RFQ, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.product_name

class Quotation(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    delivery_days = models.IntegerField()
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendor.name} - {self.total_amount}"

class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.product_name

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]

    po_number = models.CharField(max_length=50, unique=True, blank=True)
    quotation = models.OneToOneField(Quotation, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.18)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    generated_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.po_number:
            count = PurchaseOrder.objects.count() + 1
            self.po_number = f"PO-{count:05d}"
            
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=30)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.po_number

class Approval(models.Model):
    quotation = models.OneToOneField(Quotation, on_delete=models.CASCADE)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    approved = models.BooleanField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.approved:
            po, created = PurchaseOrder.objects.get_or_create(
                quotation=self.quotation,
                defaults={
                    'vendor': self.quotation.vendor,
                    'rfq': self.quotation.rfq,
                    'subtotal': self.quotation.total_amount,
                    'tax_rate': 0.18,
                    'tax_amount': float(self.quotation.total_amount) * 0.18,
                    'total_amount': float(self.quotation.total_amount) * 1.18,
                    'status': 'sent'
                }
            )

            from invoices.models import Invoice
            
            Invoice.objects.get_or_create(
                purchase_order=po,
                defaults={
                    "vendor": po.vendor,
                    "subtotal": po.subtotal,
                    "tax_amount": po.tax_amount,
                    "total_amount": po.total_amount,
                    "status": "pending",
                }
            )