from django.contrib.gis.db import models


class Cell_Types_for_Spatial_Decon(models.Model):
    cluster_id = models.CharField(max_length=8, null=True, blank=True)
    alias = models.CharField(max_length=8, null=True, blank=True)
    data_set = models.CharField(max_length=250, null=True, blank=True)
    number_of_cells = models.PositiveSmallIntegerField(null=True, blank=True)
    cell_type1 = models.CharField(max_length=125, null=True, blank=True)
    cell_type2 = models.CharField(max_length=125, null=True, blank=True)
    cell_type3 = models.CharField(max_length=125, null=True, blank=True)
    cell_type_specific = models.CharField(max_length=125, null=True, blank=True)
    cell_type_general = models.CharField(max_length=125, null=True, blank=True)
    cluster_name = models.CharField(max_length=125, null=True, blank=True)

    class Meta:
        ordering = ['-number_of_cells', 'cluster_id', ]

    # def update_celltype(self): return f'update-cell-type/{self.cluster_id}'

    def __str__(self): return self.cluster_id