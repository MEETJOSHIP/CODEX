from rest_framework import serializers
from .models import RFQ, RFQItem, Quotation, QuotationItem, Approval, PurchaseOrder
from vendors.models import Vendor

class RFQItemSerializer(serializers.ModelSerializer):
    rfqId = serializers.PrimaryKeyRelatedField(source='rfq', read_only=True)
    productName = serializers.CharField(source='product_name')
    
    class Meta:
        model = RFQItem
        fields = ['id', 'rfqId', 'productName', 'quantity', 'unit', 'description']

class RFQSerializer(serializers.ModelSerializer):
    deadline = serializers.DateField()
    createdBy = serializers.CharField(source='created_by.id', read_only=True)
    assignedVendorIds = serializers.PrimaryKeyRelatedField(source='vendors', many=True, queryset=Vendor.objects.all(), required=False)
    items = RFQItemSerializer(many=True, required=False)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = RFQ
        fields = ['id', 'title', 'description', 'status', 'deadline', 'createdBy', 'assignedVendorIds', 'items', 'createdAt']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        vendors_data = validated_data.pop('vendors', [])
        rfq = RFQ.objects.create(**validated_data)
        rfq.vendors.set(vendors_data)
        for item_data in items_data:
            RFQItem.objects.create(rfq=rfq, **item_data)
        return rfq

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        vendors_data = validated_data.pop('vendors', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if vendors_data is not None:
            instance.vendors.set(vendors_data)
            
        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                RFQItem.objects.create(rfq=instance, **item_data)
        return instance

class QuotationItemSerializer(serializers.ModelSerializer):
    quotationId = serializers.PrimaryKeyRelatedField(source='quotation', read_only=True)
    productName = serializers.CharField(source='product_name')
    unitPrice = serializers.DecimalField(source='unit_price', max_digits=10, decimal_places=2)
    totalPrice = serializers.DecimalField(source='total_price', max_digits=12, decimal_places=2)

    class Meta:
        model = QuotationItem
        fields = ['id', 'quotationId', 'productName', 'quantity', 'unitPrice', 'totalPrice']

class QuotationSerializer(serializers.ModelSerializer):
    rfqId = serializers.PrimaryKeyRelatedField(source='rfq', read_only=True)
    vendorId = serializers.PrimaryKeyRelatedField(source='vendor', read_only=True)
    totalAmount = serializers.DecimalField(source='total_amount', max_digits=12, decimal_places=2)
    deliveryDays = serializers.IntegerField(source='delivery_days')
    items = QuotationItemSerializer(many=True, read_only=True)
    submittedAt = serializers.DateTimeField(source='submitted_at', read_only=True)

    class Meta:
        model = Quotation
        fields = ['id', 'rfqId', 'vendorId', 'status', 'totalAmount', 'deliveryDays', 'notes', 'items', 'submittedAt']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    poNumber = serializers.CharField(source='po_number', read_only=True)
    quotationId = serializers.PrimaryKeyRelatedField(source='quotation', read_only=True)
    vendorId = serializers.PrimaryKeyRelatedField(source='vendor', read_only=True)
    rfqId = serializers.PrimaryKeyRelatedField(source='rfq', read_only=True)
    taxRate = serializers.DecimalField(source='tax_rate', max_digits=5, decimal_places=2)
    taxAmount = serializers.DecimalField(source='tax_amount', max_digits=12, decimal_places=2)
    totalAmount = serializers.DecimalField(source='total_amount', max_digits=12, decimal_places=2)
    generatedAt = serializers.DateTimeField(source='generated_at', read_only=True)
    dueDate = serializers.DateTimeField(source='due_date', read_only=True)
    
    items = serializers.SerializerMethodField()
    
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'poNumber', 'quotationId', 'vendorId', 'rfqId', 'status', 'items', 'subtotal', 'taxRate', 'taxAmount', 'totalAmount', 'generatedAt', 'dueDate']
        
    def get_items(self, obj):
        if obj.quotation:
            return QuotationItemSerializer(obj.quotation.items.all(), many=True).data
        return []

class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = "__all__"