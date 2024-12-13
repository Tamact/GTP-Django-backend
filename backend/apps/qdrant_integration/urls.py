from django.urls import path
from .views import StoreCVVectorsView, StoreOfferVectorView, SearchVectorsView

urlpatterns = [
    path('store_cv_vectors/', StoreCVVectorsView.as_view(), name='store-cv-vectors'),
    path('store_offer_vector/', StoreOfferVectorView.as_view(), name='store-offer-vector'),
    path('search_vectors/', SearchVectorsView.as_view(), name='search-vectors'),
]