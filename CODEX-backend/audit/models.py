from django.db import models
from django.conf import settings

class ActivityLog(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    action = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )
