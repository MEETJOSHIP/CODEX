from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

from .models import (
    RFQ,
    Quotation,
    Approval,
    PurchaseOrder,
)

from .serializers import (
    RFQSerializer,
    QuotationSerializer,
    ApprovalSerializer,
    PurchaseOrderSerializer,
)

from audit.utils import log_activity


class RFQPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role in ["procurement_officer", "admin"]


class QuotationPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role in ["vendor", "admin"]


class ApprovalPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role in ["approver", "admin"]


class RFQViewSet(viewsets.ModelViewSet):

    queryset = RFQ.objects.all()
    serializer_class = RFQSerializer
    permission_classes = [RFQPermission]

    def perform_create(self, serializer):
        rfq = serializer.save(
            created_by=self.request.user
        )
        log_activity(
            self.request.user,
            "RFQ Created",
            f"RFQ '{rfq.title}' has been created.",
            "rfq",
            rfq.id
        )

    def perform_update(self, serializer):
        rfq = serializer.save()
        log_activity(
            self.request.user,
            "RFQ Updated",
            f"RFQ '{rfq.title}' details have been updated.",
            "rfq",
            rfq.id
        )


class QuotationViewSet(viewsets.ModelViewSet):

    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    permission_classes = [QuotationPermission]

    def perform_create(self, serializer):
        q = serializer.save()
        log_activity(
            self.request.user,
            "Quotation Submitted",
            f"Quotation of ₹{q.amount:.0f} submitted by vendor for RFQ '{q.rfq.title}'.",
            "quotation",
            q.id
        )

    def perform_update(self, serializer):
        q = serializer.save()
        log_activity(
            self.request.user,
            "Quotation Updated",
            f"Quotation for RFQ '{q.rfq.title}' has been updated.",
            "quotation",
            q.id
        )


class ApprovalViewSet(viewsets.ModelViewSet):

    queryset = Approval.objects.all()
    serializer_class = ApprovalSerializer
    permission_classes = [ApprovalPermission]

    def perform_create(self, serializer):
        approval = serializer.save(
            manager=self.request.user
        )
        action_text = "Quotation Approved" if approval.approved else "Quotation Rejected"
        status_text = "approved" if approval.approved else "rejected"
        log_activity(
            self.request.user,
            action_text,
            f"Quotation for RFQ '{approval.quotation.rfq.title}' has been {status_text}.",
            "approval",
            approval.id
        )


class PurchaseOrderViewSet(
    viewsets.ReadOnlyModelViewSet
):

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]