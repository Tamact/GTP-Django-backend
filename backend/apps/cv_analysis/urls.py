from django.urls import path
from .views import CVListCreateView, CVRetrieveUpdateDeleteView

urlpatterns = [
    path('', CVListCreateView.as_view(), name='cv-list-create'),
    path('<uuid:pk>/', CVRetrieveUpdateDeleteView.as_view(), name='cv-retrieve-update-delete'),
]