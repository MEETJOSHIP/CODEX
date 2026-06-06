from django.contrib import admin

from .models import (
    RFQ,
    Quotation,
    Approval,
    PurchaseOrder
)

admin.site.register(RFQ)
admin.site.register(Quotation)
admin.site.register(Approval)
admin.site.register(PurchaseOrder)
