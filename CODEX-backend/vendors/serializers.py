from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    gstNumber = serializers.CharField(source='gst_number', required=False)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'name', 'category', 'gstNumber', 'email', 'phone', 'address', 'country', 'status', 'rating', 'createdAt']