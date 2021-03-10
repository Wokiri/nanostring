from django.contrib.gis import admin
from .models import (
    Cell_Types_for_Spatial_Decon
    )

@admin.register(Cell_Types_for_Spatial_Decon)
class Cell_Types_for_Spatial_DeconAdmin(admin.ModelAdmin):
    list_display = ['clusterID', 'number_of_cells']
    ordering = ['clusterID', 'number_of_cells']
    search_fields = ['clusterID', 'alias', 'data_set']
