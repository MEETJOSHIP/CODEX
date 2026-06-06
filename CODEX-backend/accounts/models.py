from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ADMIN = "admin"
    PROCUREMENT = "procurement_officer"
    VENDOR = "vendor"
    APPROVER = "approver"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (PROCUREMENT, "Procurement Officer"),
        (VENDOR, "Vendor"),
        (APPROVER, "Approver"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=PROCUREMENT
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    
    country = models.CharField(
        max_length=100,
        default='India'
    )
    
    profile_photo = models.URLField(
        max_length=500,
        blank=True,
        null=True
    )
    
    vendor = models.ForeignKey(
        'vendors.Vendor',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )