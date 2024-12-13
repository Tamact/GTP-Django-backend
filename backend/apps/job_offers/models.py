from django.db import models
import uuid

class JobOffer(models.Model):
    offer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text_offre = models.TextField()
    offre_societe = models.CharField(max_length=255)
    titre = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.offre_societe}"
