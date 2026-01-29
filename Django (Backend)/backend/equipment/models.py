from django.db import models


class UploadHistory(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.JSONField()

    def __str__(self):
        return f"Upload at {self.uploaded_at}"
