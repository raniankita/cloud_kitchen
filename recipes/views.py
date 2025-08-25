from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

# Create your views here.
class RecipesViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)

    def get_queryset(self):
        print(self.request.user, ">>>>>>>>>>>>>>>>")
        return Recipe.objects.filter(user=self.request.user)



