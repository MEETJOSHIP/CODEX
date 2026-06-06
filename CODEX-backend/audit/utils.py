import json
from .models import ActivityLog

def log_activity(user, action, description, target_type, target_id):
    if user and user.is_authenticated:
        payload = {
            "action": action,
            "description": description,
            "targetType": target_type,
            "targetId": str(target_id)
        }
        ActivityLog.objects.create(user=user, action=json.dumps(payload))
