from django.urls import path
from .views import JobOfferListCreateView, JobOfferRetrieveUpdateDeleteView, JobOfferCreateViewWithAnalysis

urlpatterns = [
   path('', JobOfferListCreateView.as_view(), name='job-offer-list-create'),
   path('<uuid:pk>/', JobOfferRetrieveUpdateDeleteView.as_view(), name='job-offer-retrieve-update-delete'),
  path('create_with_analysis/', JobOfferCreateViewWithAnalysis.as_view(), name='create-offer-with-analysis'),

]