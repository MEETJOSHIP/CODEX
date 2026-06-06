from rest_framework import serializers
from .models import Invoice
from procurement.serializers import QuotationItemSerializer

class InvoiceSerializer(serializers.ModelSerializer):
    invoiceNumber = serializers.CharField(source='invoice_number', read_only=True)
    poId = serializers.PrimaryKeyRelatedField(source='purchase_order', read_only=True)
    vendorId = serializers.PrimaryKeyRelatedField(source='vendor', read_only=True)
    taxAmount = serializers.DecimalField(source='tax_amount', max_digits=12, decimal_places=2)
    totalAmount = serializers.DecimalField(source='total_amount', max_digits=12, decimal_places=2)
    issuedAt = serializers.DateTimeField(source='issued_at', read_only=True)
    dueDate = serializers.DateTimeField(source='due_date', read_only=True)
    
    items = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ['id', 'invoiceNumber', 'poId', 'vendorId', 'status', 'items', 'subtotal', 'taxAmount', 'totalAmount', 'issuedAt', 'dueDate']
        
    def get_items(self, obj):
        if obj.purchase_order and obj.purchase_order.quotation:
            return QuotationItemSerializer(obj.purchase_order.quotation.items.all(), many=True).data
        return []