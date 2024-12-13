from django.db import models
import uuid

class Profile(models.Model):
    profil_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profil = models.CharField(max_length=255)
    question = models.JSONField(default=list)
    
    def __str__(self):
        return self.profil