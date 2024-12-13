from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import extract_text_from_pdf
import logging

logger = logging.getLogger(__name__)
class ExtractTextView(APIView):
    def post(self, request):
        pdf_file = request.FILES.get('pdf_file')
        if not pdf_file:
             logger.error("Pas de fichier pdf reçu")
             return Response({'error': 'No PDF file provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            text = extract_text_from_pdf(pdf_file)
            return Response({'text': text}, status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(f"Erreur lors du traitement du pdf:{e}")
             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)