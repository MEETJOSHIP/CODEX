import os
import sys
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vendorbridge.settings")
django.setup()

from django.contrib.auth import get_user_model
from vendors.models import Vendor
from procurement.models import RFQ, RFQItem, Quotation, QuotationItem, PurchaseOrder, Approval
from invoices.models import Invoice

User = get_user_model()

def seed():
    print("Clearing old data...")
    Invoice.objects.all().delete()
    PurchaseOrder.objects.all().delete()
    Approval.objects.all().delete()
    Quotation.objects.all().delete()
    RFQ.objects.all().delete()
    Vendor.objects.all().delete()
    User.objects.all().delete()

    print("Creating users...")
    admin = User.objects.create_superuser(username="admin@codex.com", email="admin@codex.com", password="password", first_name="System", last_name="Admin", role="admin")
    procurement = User.objects.create_user(username="procurement@codex.com", email="procurement@codex.com", password="password", first_name="Jay", last_name="Josh", role="procurement_officer")
    approver = User.objects.create_user(username="approver@codex.com", email="approver@codex.com", password="password", first_name="Sarah", last_name="Manager", role="approver")

    print("Creating vendors...")
    v1 = Vendor.objects.create(name="TechCorp India", category="IT Equipment", email="sales@techcorp.in", phone="9876543210", gst_number="27AAAAA1234A1Z5", status="active")
    v2 = Vendor.objects.create(name="OfficeSupplies Co", category="Stationery", email="hello@officesup.com", phone="9123456789", gst_number="27BBBBB1234B1Z5", status="active")
    v3 = Vendor.objects.create(name="Global Networks", category="IT Equipment", email="contact@globalnet.com", phone="9988776655", gst_number="27CCCCC1234C1Z5", status="pending")

    vendor_user = User.objects.create_user(username="sales@techcorp.in", email="sales@techcorp.in", password="password", first_name="Vendor", last_name="TechCorp", role="vendor", vendor_id=v1.id)

    print("Creating RFQs...")
    now = timezone.now()
    rfq1 = RFQ.objects.create(title="New Laptops for Engineering", description="We need 10 high-end laptops.", deadline=(now + timedelta(days=14)).date(), created_by=procurement, status="sent")
    rfq1.vendors.set([v1, v3])
    RFQItem.objects.create(rfq=rfq1, product_name="MacBook Pro 16", quantity=10, unit="pcs", description="M3 Max, 36GB RAM")

    rfq2 = RFQ.objects.create(title="Office Stationery Restock", description="Pens, paper, and staplers.", deadline=(now + timedelta(days=5)).date(), created_by=procurement, status="sent")
    rfq2.vendors.set([v2])
    RFQItem.objects.create(rfq=rfq2, product_name="A4 Printer Paper", quantity=50, unit="boxes")
    RFQItem.objects.create(rfq=rfq2, product_name="Blue Pens", quantity=200, unit="pcs")

    rfq3 = RFQ.objects.create(title="Server Upgrades", description="Need new server racks.", deadline=(now - timedelta(days=2)).date(), created_by=procurement, status="closed")
    rfq3.vendors.set([v1])
    RFQItem.objects.create(rfq=rfq3, product_name="Dell PowerEdge", quantity=2, unit="pcs")

    print("Creating Quotations & Approvals...")
    q1 = Quotation.objects.create(rfq=rfq1, vendor=v1, status="submitted", delivery_days=10, notes="Includes 3-year warranty.", total_amount=2500000)
    QuotationItem.objects.create(quotation=q1, product_name="MacBook Pro 16", quantity=10, unit_price=250000, total_price=2500000)

    q2 = Quotation.objects.create(rfq=rfq2, vendor=v2, status="accepted", delivery_days=2, notes="Same day dispatch available.", total_amount=15000)
    QuotationItem.objects.create(quotation=q2, product_name="A4 Printer Paper", quantity=50, unit_price=200, total_price=10000)
    QuotationItem.objects.create(quotation=q2, product_name="Blue Pens", quantity=200, unit_price=25, total_price=5000)

    app1 = Approval.objects.create(quotation=q2, manager=approver, approved=True, comment="Looks good, approved.")

    print("Creating Purchase Orders & Invoices...")
    # Approval automatically creates PO and Invoice in the save() signal!
    po = PurchaseOrder.objects.first()
    if po:
        po.status = "sent"
        po.save()
        inv = Invoice.objects.filter(purchase_order=po).first()
        if inv:
            inv.status = "pending"
            inv.save()

    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
