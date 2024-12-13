from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import generate_questionnaire_google, categorize_skills_with_kano, detect_ai_generated_text, analyze_text_style
import logging
logger = logging.getLogger(__name__)

class GenerateQuestionnaireView(APIView):
    def post(self, request):
        profil = request.data.get('profil')
        if not profil:
            logger.error("Le profil est manquant")
            return Response({'error': 'profil is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            questions = generate_questionnaire_google(profil)
            if questions:
                return Response({'questions': questions}, status=status.HTTP_200_OK)
            else :
                logger.error("Aucune question générée")
                return Response({'message':'Aucune question générée'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             logger.error(f"Erreur lors de la génération des questions: {e}")
             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategorizeSkillsView(APIView):
    def post(self, request):
        offre_text = request.data.get('offre_text')
        if not offre_text:
            logger.error("Le texte de l'offre est manquant")
            return Response({'error': 'offer_text is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            categorized_skills = categorize_skills_with_kano(offre_text)
            if categorized_skills:
                return Response({'categorized_skills': categorized_skills}, status=status.HTTP_200_OK)
            else:
                logger.error("La catégorisation des compétences a échoué")
                return Response({'message': 'Failed to categorize skills'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Erreur lors de la catégorisation des compétences:{e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DetectAIGeneratedTextView(APIView):
     def post(self, request):
        text = request.data.get('text')
        if not text:
            logger.error("Le texte est manquant")
            return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = detect_ai_generated_text(text)
            if result:
                return Response({'result': result}, status=status.HTTP_200_OK)
            else:
                logger.error("Erreur lors de la détection IA.")
                return Response({'message': 'AI detection failed'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Erreur lors de la détection IA:{e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AnalyzeTextStyleView(APIView):
     def post(self, request):
        text = request.data.get('text')
        if not text:
            logger.error("Le texte est manquant.")
            return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            analysis = analyze_text_style(text)
            if analysis:
                return Response({'analysis': analysis}, status=status.HTTP_200_OK)
            else:
                logger.error("Erreur lors de l'analyse du style du texte.")
                return Response({'message': 'Text analysis failed'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse du style du texte:{e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)