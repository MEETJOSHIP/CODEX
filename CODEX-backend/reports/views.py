from rest_framework.views import APIView
from rest_framework.response import Response

from vendors.models import Vendor
from procurement.models import (
    RFQ,
    Quotation,
    Approval,
    PurchaseOrder,
)
from invoices.models import Invoice


class DashboardView(APIView):

    def get(self, request):

        return Response({

            "vendors":
                Vendor.objects.count(),

            "rfqs":
                RFQ.objects.count(),

            "quotations":
                Quotation.objects.count(),

            "approvals":
                Approval.objects.count(),

            "purchase_orders":
                PurchaseOrder.objects.count(),

            "invoices":
                Invoice.objects.count(),
        })