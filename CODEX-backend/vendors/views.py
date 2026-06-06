from rest_framework import viewsets
from .models import Vendor
from .serializers import VendorSerializer
from audit.utils import log_activity

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def perform_create(self, serializer):
        vendor = serializer.save()
        log_activity(
            self.request.user,
            "Vendor Added",
            f"Vendor {vendor.name} has been added to the system.",
            "vendor",
            vendor.id
        )

    def perform_update(self, serializer):
        vendor = serializer.save()
        log_activity(
            self.request.user,
            "Vendor Updated",
            f"Vendor {vendor.name} details have been updated.",
            "vendor",
            vendor.id
        )
