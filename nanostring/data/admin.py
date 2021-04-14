from django.contrib.gis import admin
from .models import (
    Category,
    Cell_Types_for_Spatial_Decon,
    Kidney_Sample_Annotations,
    RawCSVFiles,
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

admin.site.register(Category, CategoryAdmin)



@admin.register(Cell_Types_for_Spatial_Decon)
class Cell_Types_for_Spatial_DeconAdmin(admin.ModelAdmin):
    list_display = ['cluster_id', 'number_of_cells']
    list_filter = ['data_set', 'cell_type_general',]
    ordering = ['cluster_id', 'number_of_cells']
    search_fields = ['cluster_id', 'alias', 'data_set']


@admin.register(Kidney_Sample_Annotations)
class Kidney_Sample_Annotations(admin.ModelAdmin):
    list_display = ['scan_name', 'roi_label', 'segment_label',]
    list_filter = ['slide_name', 'scan_name',]
    ordering = ['roi_label', 'scan_name']
    search_fields = ['slide_name', 'scan_name', 'roi_label', 'segment_label',]



admin.site.register(RawCSVFiles)