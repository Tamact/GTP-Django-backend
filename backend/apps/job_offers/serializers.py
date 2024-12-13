from rest_framework import serializers
from .models import JobOffer

class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = ['offer_id', 'text_offre', 'offre_societe', 'titre', 'created_at']