from rest_framework import generics
from .models import Result
from .serializers import ResultSerializer
from rest_framework.response import Response
from rest_framework import status
from .service import calculate_and_save_similarity
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

class ResultListCreateView(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

class ResultRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    

class CalculateSimilarityView(generics.GenericAPIView):
     def post(self, request):
        cv_id = request.data.get('cv_id')
        offer_id = request.data.get('offer_id')
        if not cv_id or not offer_id:
            logger.error("cv_id and offer_id are required")
            return Response({'error': 'cv_id and offer_id are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = calculate_and_save_similarity(cv_id, offer_id)
            serializer = ResultSerializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Erreur lors du calcul de la similarité: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FilterResultsView(generics.ListAPIView):
    serializer_class = ResultSerializer
    def get_queryset(self):
        queryset = Result.objects.all()
        skills = self.request.query_params.get('skills')
        similarity_threshold = self.request.query_params.get('similarity_threshold')
        num_results = self.request.query_params.get('num_results')

        if skills:
            skills_list = [skill.strip() for skill in skills.split(",")]
            queryset = queryset.filter(cv__competences__contains=skills_list)
        if similarity_threshold:
            try:
               threshold = float(similarity_threshold)
               queryset = queryset.filter(cosine_similarity__gte=threshold)
            except ValueError:
                logger.error("Erreur lors de la conversion du seuil de similarité")
                pass
        if num_results:
            try:
                limit = int(num_results)
                queryset= queryset[:limit]
            except ValueError:
                 logger.error("Erreur lors de la conversion du nombre de résultats")
                 pass

        return queryset