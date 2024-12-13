from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import store_vectors_in_qdrant, store_offer_vector_in_qdrant, search_vectors_in_qdrant
import numpy as np
import logging

logger = logging.getLogger(__name__)

class StoreCVVectorsView(APIView):
    def post(self, request):
        vectors_data = request.data.get('vectors')
        names = request.data.get('names')
        if not vectors_data or not names:
            logger.error("Vecteurs ou noms de CV manquants.")
            return Response({'error': 'Vectors and names are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            vectors = [np.array(vec) for vec in vectors_data]
            store_vectors_in_qdrant(vectors, names)
            return Response({'message': 'CV vectors stored successfully in Qdrant'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Erreur lors du stockage des vecteurs de CV dans Qdrant: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StoreOfferVectorView(APIView):
    def post(self, request):
        vector = request.data.get('vector')
        offer_name = request.data.get('offer_name')
        if not vector or not offer_name:
           logger.error("Vecteur ou nom de l'offre d'emploi manquant")
           return Response({'error': 'Vector and offer_name are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
             vector_array = np.array(vector)
             store_offer_vector_in_qdrant(vector_array, offer_name)
             return Response({'message': 'Offer vector stored successfully in Qdrant'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Erreur lors du stockage du vecteur de l'offre d'emploi dans Qdrant: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchVectorsView(APIView):
    def post(self, request):
        query_vector_data = request.data.get('query_vector')
        collection_name = request.data.get('collection_name', 'cv_collection')
        limit = request.data.get('limit', 5)
        if not query_vector_data:
            logger.error("Vecteur de recherche manquant.")
            return Response({'error': 'Query vector is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            query_vector = np.array(query_vector_data)
            results = search_vectors_in_qdrant(query_vector, collection_name, limit)
            if results:
                return Response({'results': [res.payload for res in results]}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No matching vectors found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           logger.error(f"Erreur lors de la recherche des vecteurs dans Qdrant: {e}")
           return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)