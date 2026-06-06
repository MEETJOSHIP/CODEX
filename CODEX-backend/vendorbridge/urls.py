from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from accounts.views import CustomTokenObtainPairView, RegisterView

urlpatterns = [

    path("admin/", admin.site.urls),

    path(
        "api/token/",
        CustomTokenObtainPairView.as_view()
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view()
    ),

    path(
        "api/register/",
        RegisterView.as_view()
    ),

    path(
        "api/vendors/",
        include("vendors.urls")
    ),

    path(
        "api/procurement/",
        include("procurement.urls")
    ),

    path(
        "api/reports/",
        include("reports.urls")
    ),

    path(
        "api/audit/",
        include("audit.urls")
    ),

    path(
        "api/",
        include("invoices.urls")
    ),

]