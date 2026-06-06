from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add custom response fields
        data['id'] = self.user.id
        data['firstName'] = self.user.first_name
        data['lastName'] = self.user.last_name
        data['email'] = self.user.email
        data['role'] = self.user.role
        data['phone'] = self.user.phone
        data['country'] = self.user.country
        data['profilePhoto'] = self.user.profile_photo
        data['vendorId'] = self.user.vendor_id
        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    firstName = serializers.CharField(source='first_name', required=False, allow_blank=True)
    lastName = serializers.CharField(source='last_name', required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["email", "password", "firstName", "lastName", "role", "phone", "country"]

    def create(self, validated_data):
        email = validated_data.get("email")
        validated_data["username"] = email  # use email as username
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # If role is vendor, auto-create a Vendor profile matching this user
        if user.role == "vendor":
            from vendors.models import Vendor
            import random
            import string
            
            # Generate a unique GST placeholder number
            gst = "27" + "".join(random.choices(string.ascii_uppercase + string.digits, k=13))
            
            Vendor.objects.get_or_create(
                email=user.email,
                defaults={
                    "name": f"{user.first_name} {user.last_name}".strip() or "New Vendor",
                    "phone": user.phone or "",
                    "gst_number": gst,
                    "category": "General",
                    "status": "active"
                }
            )
        return user
