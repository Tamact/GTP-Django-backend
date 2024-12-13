from rest_framework import generics
from .models import JobOffer
from .serializers import JobOfferSerializer
from rest_framework.response import Response
from rest_framework import status

class JobOfferListCreateView(generics.ListCreateAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    

class JobOfferRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer