from django.contrib.gis import admin
from .models import (
    Cell_Types_for_Spatial_Decon
    )

@admin.register(Cell_Types_for_Spatial_Decon)
class Cell_Types_for_Spatial_DeconAdmin(admin.ModelAdmin):
    list_display = ['cluster_id', 'number_of_cells']
    ordering = ['cluster_id', 'number_of_cells']
    search_fields = ['cluster_id', 'alias', 'data_set']
