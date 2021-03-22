from django.contrib.gis.db import models

class Category(models.Model):
    name = models.CharField('Name of category', max_length=25, null=True, blank=True)
    description = models.CharField('Brief description about the category', max_length=125, null=True, blank=True)
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Kidney_Sample_Annotations(models.Model):
    slide_name = models.CharField(max_length=25, null=True, blank=True)
    scan_name = models.CharField(max_length=50, null=True, blank=True)
    roi_label = models.PositiveSmallIntegerField(null=True, blank=True)
    segment_label = models.CharField(max_length=125, null=True, blank=True)
    segment_display_name = models.CharField(max_length=250, null=True, blank=True)
    sample_id = models.CharField(max_length=125, null=True, blank=True)
    aoi_surface_area = models.FloatField(null=True, blank=True)
    aoi_nuclei_count = models.PositiveSmallIntegerField(null=True, blank=True) # Values from 0 to 32767 are safe in all databases supported by Django.
    roi_coordinate_x = models.IntegerField(null=True, blank=True) # Values from -2147483648 to 2147483647 are safe in all databases supported by Django.
    roi_coordinate_y = models.IntegerField(null=True, blank=True) # Values from -2147483648 to 2147483647 are safe in all databases supported by Django.
    raw_reads = models.IntegerField(null=True, blank=True) 
    trimmed_reads = models.IntegerField(null=True, blank=True)
    stitched_reads = models.IntegerField(null=True, blank=True)
    aligned_reads = models.IntegerField(null=True, blank=True)
    duplicated_reads = models.IntegerField(null=True, blank=True)
    sequencing_saturation = models.FloatField(null=True, blank=True)
    umiq_30 = models.FloatField(null=True, blank=True)
    rtsq_30 = models.FloatField(null=True, blank=True)
    disease_status = models.CharField(max_length=25, null=True, blank=True)
    pathology = models.CharField(max_length=25, null=True, blank=True)
    region = models.CharField(max_length=25, null=True, blank=True)
    loq = models.FloatField(null=True, blank=True)
    normalization_factor = models.FloatField(null=True, blank=True)
    geom = models.PointField(srid=3857, null=True, blank=True)


    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="category of data"
        )

    class Meta:
        ordering = ['roi_label']
        verbose_name = 'sample annotation'
        verbose_name_plural = 'sample annotations'

    def __str__(self): return f'{self.roi_label}: {self.slide_name}'
    


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

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="category of data"
        )


    class Meta:
        ordering = ['-number_of_cells', 'cluster_id', ]
        verbose_name = 'cell type'
        verbose_name_plural = 'cell annotations (cell types)'


    def __str__(self): return self.cluster_id


class Kidney_Feature_Annotation(models.Model):
    rts_id = models.CharField(max_length=25, null=True, blank=True)
    target_name = models.CharField(max_length=25, null=True, blank=True)
    probe_id = models.IntegerField(null=True, blank=True)
    negative = models.BooleanField(null=True, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="category of data"
        )


    class Meta:
        ordering = ['probe_id', ]
        verbose_name = 'kidney feature annotation'
        verbose_name_plural = 'kidney feature annotations'


    def __str__(self): return self.rts_id