from django.urls import path
from .views import CandidateListCreateView, CandidateRetrieveUpdateDeleteView, CheckCandidateConnexion, GenerateCodeView, RegisterCandidateWithAnalysisView #UpdateCandidateEvaluationView

urlpatterns = [
    path('', CandidateListCreateView.as_view(), name='candidate-list-create'),
    path('<uuid:pk>/', CandidateRetrieveUpdateDeleteView.as_view(), name='candidate-retrieve-update-delete'),
    path('connexion/', CheckCandidateConnexion.as_view(), name='candidate-check-connexion'),
    path('generate_code/', GenerateCodeView.as_view(), name='candidate-generate-code'),
    #path('update_evaluation/', UpdateCandidateEvaluationView.as_view(), name='candidate-update-evaluation'),
    path('register_with_analysis/', RegisterCandidateWithAnalysisView.as_view(), name='register-candidate-with-analysis')

]