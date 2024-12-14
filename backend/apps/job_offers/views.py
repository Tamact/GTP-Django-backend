from rest_framework import generics
from .models import JobOffer
from .serializers import JobOfferSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.users.service import preprocess_text
import logging

logger = logging.getLogger(__name__)
class JobOfferListCreateView(generics.ListCreateAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer


class JobOfferRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer

class JobOfferCreateViewWithAnalysis(generics.GenericAPIView):
    def post(self, request):
        titre = request.data.get('titre')
        offre_societe = request.data.get('offre_societe')
        text_offre = request.data.get('text_offre')
        if not titre or not offre_societe or not text_offre:
             logger.error("Le titre, le nom de la société et le texte de l'offre sont requis")
             return Response({'error': 'titre, offre_societe and text_offre are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # 1. Prétraitement du texte de l'offre
            preprocessed_offre_text = preprocess_text(text_offre)
            # 2. Enregistrement de l'offre
            job_offer = JobOffer.objects.create(titre=titre, offre_societe=offre_societe, text_offre=preprocessed_offre_text)
            if not job_offer :
                  logger.error("Erreur lors de l'enregistrement de l'offre d'emploi")
                  return Response({'error': 'Erreur lors de l\'enregistrement de l\'offre d\'emploi'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Job offer created with preprocessed text successfully', 'offer_id': job_offer.offer_id}, status=status.HTTP_201_CREATED)

        except Exception as e:
              logger.error(f"Une erreur s'est produite: {e}")
              return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)