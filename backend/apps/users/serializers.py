from rest_framework import serializers
from .models import Candidate

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['user_id', 'nom_prenom', 'mail', 'numero_tlfn', 'profil', 'code']