from django.urls import path
from .views import Cell_Types_for_Spatial_DeconAPIView

app_name = 'api'

urlpatterns = [
path('', Cell_Types_for_Spatial_DeconAPIView.as_view()),
]