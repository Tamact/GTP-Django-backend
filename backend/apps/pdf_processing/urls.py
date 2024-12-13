from django.urls import path
from .views import ExtractTextView

urlpatterns = [
    path('extract/', ExtractTextView.as_view(), name='extract-text'),
]