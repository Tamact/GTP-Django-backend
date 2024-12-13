from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework import status

class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
class CheckProfileView(generics.GenericAPIView):
     def post(self, request):
        profil = request.data.get('profil')
        if not profil:
            return Response({'error': 'profil is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            profile = Profile.objects.get(profil=profil)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            new_profile = Profile.objects.create(profil=profil)
            serializer = ProfileSerializer(new_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)