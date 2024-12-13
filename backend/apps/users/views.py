from django.shortcuts import render
from rest_framework import generics
from .models import Candidate
from .serializers import CandidateSerializer
from rest_framework.response import Response
from rest_framework import status
import random
import string

class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    
class CandidateRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CheckCandidateConnexion(generics.GenericAPIView):
    def post(self, request):
        mail = request.data.get('mail')
        code = request.data.get('code')
        if not mail or not code:
            return Response({'error': 'mail and code are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            candidate = Candidate.objects.get(mail=mail, code=code)
            serializer = CandidateSerializer(candidate)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Candidate.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class GenerateCodeView(generics.GenericAPIView):
    def post(self, request):
        mail = request.data.get('mail')
        profil = request.data.get('profil')
        if not mail or not profil:
            return Response({'error': 'mail and profil are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            candidate = Candidate.objects.get(mail=mail)
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            candidate.code = code
            candidate.profil = profil
            candidate.save()

            # Envoi de mail (pas implémenté, à faire avec Celery)
            return Response({'message': 'Code généré et envoyé par e-mail', 'code': code}, status=status.HTTP_200_OK)
        except Candidate.DoesNotExist:
            return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)
