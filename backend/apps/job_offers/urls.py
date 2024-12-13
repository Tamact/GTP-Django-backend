from django.urls import path
from .views import JobOfferListCreateView, JobOfferRetrieveUpdateDeleteView

urlpatterns = [
    path('', JobOfferListCreateView.as_view(), name='job-offer-list-create'),
    path('<uuid:pk>/', JobOfferRetrieveUpdateDeleteView.as_view(), name='job-offer-retrieve-update-delete'),
]