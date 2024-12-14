from django.shortcuts import render
from rest_framework import generics
from .models import Candidate
from .serializers import CandidateSerializer
from rest_framework.response import Response
from rest_framework import status
import random
import string
from rest_framework.views import APIView
from apps.pdf_processing.service import extract_text_from_pdf
from apps.ai_integration.services import analyze_text_style, detect_ai_generated_text
from .service import preprocess_text
from apps.cv_analysis.models import CV
import logging 

logger = logging.getLogger(__name__) 

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

 #Option 2
class RegisterCandidateWithAnalysisView(APIView):
    def post(self, request):
        pdf_file = request.FILES.get('pdf_file')
        nom_prenom = request.data.get('nom_prenom')
        mail = request.data.get('mail')
        numero_tlfn= request.data.get('numero_tlfn')
        if not pdf_file or not nom_prenom or not mail:
                logger.error("Fichier PDF, nom_prenom, mail sont requis")
                return Response({'error': 'pdf_file, nom_prenom and mail are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # 1. Extraction du texte du PDF
            cv_text = extract_text_from_pdf(pdf_file)
            if not cv_text :
                logger.error("Impossible d'extraire le texte du pdf")
                return Response({'error': 'Impossible d\'extraire le texte du pdf'}, status=status.HTTP_400_BAD_REQUEST)

            # 2. Analyse du style du texte
            style_analysis = analyze_text_style(cv_text)
            if not style_analysis :
                    logger.error("Erreur lors de l'analyse du style du texte")
                    return Response({'error': 'Erreur lors de l\'analyse du style du texte'}, status=status.HTTP_400_BAD_REQUEST)

            # 3. Détection IA
            ai_detection = detect_ai_generated_text(cv_text)
            if not ai_detection:
                logger.error("Erreur lors de la détection IA")
                return Response({'error': 'Erreur lors de la détection IA'}, status=status.HTTP_400_BAD_REQUEST)

                #4. Prétraitement du texte
            preprocessed_cv_text = preprocess_text(cv_text)
            # 5. Enregistrement du candidat
            candidate = Candidate.objects.create(nom_prenom=nom_prenom, mail=mail, numero_tlfn=numero_tlfn)
            if not candidate:
                logger.error("Erreur lors de l'enregistrement du candidat")
                return Response({'error': 'Erreur lors de l\'enregistrement du candidat'}, status=status.HTTP_400_BAD_REQUEST)

            # 6. Enregistrement du CV
            cv = CV.objects.create(user=candidate, cv_text=preprocessed_cv_text)
            if not cv :
                logger.error("Erreur lors de l'enregistrement du cv")
                return Response({'error': 'Erreur lors de l\'enregistrement du cv'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                            'message': 'Candidate and CV registered successfully',
                            'style_analysis': style_analysis,
                            'ai_detection': ai_detection,
                                'candidate_id':candidate.user_id,
                                'cv_id': cv.cv_id,
                            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Une erreur s'est produite: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)