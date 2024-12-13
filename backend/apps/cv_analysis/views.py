from rest_framework import generics
from .models import CV
from .serializers import CVSerializer
from rest_framework.response import Response
from rest_framework import status


class CVListCreateView(generics.ListCreateAPIView):
    queryset = CV.objects.all()
    serializer_class = CVSerializer

class CVRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CV.objects.all()
    serializer_class = CVSerializer