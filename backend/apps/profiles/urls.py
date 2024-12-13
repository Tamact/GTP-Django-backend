from django.urls import path
from .views import ProfileListCreateView, ProfileRetrieveUpdateDeleteView, CheckProfileView

urlpatterns = [
    path('', ProfileListCreateView.as_view(), name='profile-list-create'),
    path('<uuid:pk>/', ProfileRetrieveUpdateDeleteView.as_view(), name='profile-retrieve-update-delete'),
    path('check_profile/', CheckProfileView.as_view(), name='profile-check'),

]