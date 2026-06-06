from rest_framework.routers import DefaultRouter

from .views import VendorViewSet

router = DefaultRouter()

router.register(
    "vendors",
    VendorViewSet
)

urlpatterns = router.urls