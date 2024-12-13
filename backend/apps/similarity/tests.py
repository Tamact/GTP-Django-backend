from django.test import TestCase
from apps.cv_analysis.models import CV
from apps.job_offers.models import JobOffer
from apps.similarity.models import Result
from apps.similarity.service import calculate_and_save_similarity
from apps.users.models import Candidate
from rest_framework import status
from rest_framework.test import APIClient

class SimilarityServicesTests(TestCase):
    def setUp(self):
        # Créer des instances de test
        self.candidate = Candidate.objects.create(nom_prenom="Test User", mail="test@test.com")
        self.cv = CV.objects.create(user=self.candidate, cv_text="Python, data science, machine learning")
        self.offer = JobOffer.objects.create(titre="Data Scientist", offre_societe="Tech Corp", text_offre="Python, data science, statistics")

    def test_calculate_and_save_similarity(self):
        # Tester le calcul de similarité et l'enregistrement
        result = calculate_and_save_similarity(self.cv.cv_id, self.offer.offer_id)
        self.assertIsInstance(result, Result)
        self.assertIsNotNone(result.cosine_similarity)

class SimilarityApiTests(TestCase):
        def setUp(self):
             self.client = APIClient()
             self.candidate = Candidate.objects.create(nom_prenom="Test User", mail="test@test.com")
             self.cv = CV.objects.create(user=self.candidate, cv_text="Python, data science, machine learning",competences = ["Python","Data science", "Machine learning"])
             self.offer = JobOffer.objects.create(titre="Data Scientist", offre_societe="Tech Corp", text_offre="Python, data science, statistics")
             self.result = Result.objects.create(cv=self.cv, offer=self.offer, cosine_similarity=0.8)
    
        def test_filter_results_by_skills(self):
              url = f'/api/results/filter/?skills=Python,Data%20science'
              response = self.client.get(url)
              self.assertEqual(response.status_code, status.HTTP_200_OK)
              self.assertEqual(len(response.data), 1)
              self.assertEqual(response.data[0]['cv'], str(self.cv.cv_id))


        def test_filter_results_by_threshold(self):
            url = f'/api/results/filter/?similarity_threshold=0.7'
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['cosine_similarity'], 0.8)
        def test_filter_results_by_limit(self):
           url = f'/api/results/filter/?num_results=1'
           response = self.client.get(url)
           self.assertEqual(response.status_code, status.HTTP_200_OK)
           self.assertEqual(len(response.data), 1)