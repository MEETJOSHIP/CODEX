from rest_framework.routers import DefaultRouter

from .views import (
    RFQViewSet,
    QuotationViewSet,
    ApprovalViewSet,
    PurchaseOrderViewSet
)

router = DefaultRouter()

router.register("rfqs", RFQViewSet)
router.register("quotations", QuotationViewSet)
router.register("approvals", ApprovalViewSet)
router.register(
    "purchase-orders",
    PurchaseOrderViewSet
)

urlpatterns = router.urls