from django.db import models
from apps.users.models import Candidate
import uuid

class CV(models.Model):
    cv_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='cvs')
    date_insertion = models.DateTimeField(auto_now_add=True)
    cv_text = models.TextField()
    competences = models.JSONField(default=list)
    
    def __str__(self):
        return f"CV for {self.user.nom_prenom} - {self.date_insertion}"
