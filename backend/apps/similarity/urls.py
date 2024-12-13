from django.urls import path
from .views import ResultListCreateView, ResultRetrieveUpdateDeleteView, CalculateSimilarityView, FilterResultsView

urlpatterns = [
    path('', ResultListCreateView.as_view(), name='result-list-create'),
    path('<uuid:pk>/', ResultRetrieveUpdateDeleteView.as_view(), name='result-retrieve-update-delete'),
    path('calculate_similarity/', CalculateSimilarityView.as_view(), name='calculate-similarity'),
    path('filter/', FilterResultsView.as_view(), name='filter-results'),
]