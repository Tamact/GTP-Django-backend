from django.db import models
from apps.cv_analysis.models import CV
from apps.job_offers.models import JobOffer
import uuid


class Result(models.Model):
    result_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='results')
    offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name='results')
    cosine_similarity = models.FloatField()
    
    def __str__(self):
        return f"Similarity between {self.cv} and {self.offer} : {self.cosine_similarity}"