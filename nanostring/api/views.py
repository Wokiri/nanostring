from rest_framework import generics
from data.models import Cell_Types_for_Spatial_Decon
from .serializers import Cell_Types_for_Spatial_Decon_Serializer

class Cell_Types_for_Spatial_DeconAPIView(generics.ListAPIView):
    queryset = Cell_Types_for_Spatial_Decon.objects.all()
    serializer_class = Cell_Types_for_Spatial_Decon_Serializer