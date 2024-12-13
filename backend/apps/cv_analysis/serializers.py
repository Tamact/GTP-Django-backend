from rest_framework import serializers
from .models import CV

class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = ['cv_id', 'user', 'date_insertion', 'cv_text', 'competences']