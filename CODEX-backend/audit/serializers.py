from rest_framework import serializers
from .models import ActivityLog

class ActivityLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    performed_by_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ActivityLog
        fields = ["id", "user", "username", "performed_by_name", "action", "timestamp"]

    def get_performed_by_name(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
        return ""
