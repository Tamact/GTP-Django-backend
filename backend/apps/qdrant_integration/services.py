import os
import uuid
import logging
from qdrant_client import QdrantClient
from django.conf import settings
import numpy as np


logger = logging.getLogger(__name__)

def get_qdrant_client():
    """Initialisation du client Qdrant."""
    client = QdrantClient(
        url=os.getenv("QDRANT_HOST"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    return client

def store_vectors_in_qdrant(vectors, names, collection_name="cv_collection"):
    """Stockage des vecteurs dans Qdrant."""
    client = get_qdrant_client()
    points = [
        {
            "id": str(uuid.uuid4()),
            "vector": vector.tolist(),
            "payload": {"name": name}
        }
        for name, vector in zip(names, vectors)
    ]
    try:
        client.upsert(collection_name=collection_name, points=points)
        logger.info(f"Vecteurs stockés avec succès dans Qdrant. Collection: {collection_name}")
        return True
    except Exception as e:
        logger.error(f"Erreur lors du stockage des vecteurs dans Qdrant: {e}")
        return False

def store_offer_vector_in_qdrant(offer_vector, offer_name, collection_name="offer_collection"):
    """Stockage du vecteur de l'offre d'emploi dans Qdrant."""
    client = get_qdrant_client()
    point = {
        "id": str(uuid.uuid4()),
        "vector": offer_vector.tolist(),
        "payload": {"name": offer_name}
    }

    try:
        client.upsert(
            collection_name=collection_name,
            points=[point]
        )
        logger.info(f"Vecteur de l'offre d'emploi stocké avec succès dans Qdrant. Collection: {collection_name}")
        return True
    except Exception as e:
        logger.error(f"Erreur lors du stockage du vecteur de l'offre d'emploi dans Qdrant: {e}")
        return False


def search_vectors_in_qdrant(query_vector, collection_name="cv_collection", limit=5):
    """Recherche les vecteurs similaires dans Qdrant."""
    client = get_qdrant_client()
    try:
        search_result = client.search(
            collection_name=collection_name,
            query_vector=query_vector.tolist(),
            limit=limit
        )
        logger.info("Recherche de vecteurs dans Qdrant effectuée avec succès.")
        return search_result
    except Exception as e:
        logger.error(f"Erreur lors de la recherche des vecteurs dans Qdrant: {e}")
        return None