# Generated by Django 3.1.4 on 2021-04-10 04:13

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=25, null=True, verbose_name='Name of category')),
                ('description', models.CharField(blank=True, max_length=125, null=True, verbose_name='Brief description about the category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Disease1BScanVector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fid', models.FloatField()),
                ('dn', models.BigIntegerField()),
                ('name', models.CharField(blank=True, max_length=254, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='RawCSVFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(blank=True, choices=[('KidneySampleAnnotations', 'Kidney_Sample_Annotations.csv'), ('KidneyFeatureAnnotations', 'Kidney_Feature_Annotations.csv'), ('KidneyRawBioProbeCountMatrix', 'Kidney_Raw_BioProbeCountMatrix.csv'), ('KidneyRawTargetCountMatrix', 'Kidney_Raw_TargetCountMatrix.csv'), ('KidneyQ3NormTargetCountMatrix', 'Kidney_Q3Norm_TargetCountMatrix.csv'), ('CellTypesforSpatialDecon', 'Cell_Types_for_Spatial_Decon.csv'), ('AverageGeneExpression', 'Young_kidney_cell_profile_matrix.csv'), ('KidneyssGSEA', 'Kidney_ssGSEA.csv')], max_length=125, null=True)),
                ('file', models.FileField(upload_to='csv_uploads/')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.category', verbose_name='category of data')),
            ],
        ),
        migrations.CreateModel(
            name='Kidney_Sample_Annotations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slide_name', models.CharField(blank=True, max_length=25, null=True)),
                ('scan_name', models.CharField(blank=True, max_length=50, null=True)),
                ('roi_label', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('segment_label', models.CharField(blank=True, max_length=125, null=True)),
                ('segment_display_name', models.CharField(blank=True, max_length=250, null=True)),
                ('sample_id', models.CharField(blank=True, max_length=125, null=True)),
                ('aoi_surface_area', models.FloatField(blank=True, null=True)),
                ('aoi_nuclei_count', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('roi_coordinate_x', models.IntegerField(blank=True, null=True)),
                ('roi_coordinate_y', models.IntegerField(blank=True, null=True)),
                ('raw_reads', models.IntegerField(blank=True, null=True)),
                ('trimmed_reads', models.IntegerField(blank=True, null=True)),
                ('stitched_reads', models.IntegerField(blank=True, null=True)),
                ('aligned_reads', models.IntegerField(blank=True, null=True)),
                ('duplicated_reads', models.IntegerField(blank=True, null=True)),
                ('sequencing_saturation', models.FloatField(blank=True, null=True)),
                ('umiq_30', models.FloatField(blank=True, null=True)),
                ('rtsq_30', models.FloatField(blank=True, null=True)),
                ('disease_status', models.CharField(blank=True, max_length=25, null=True)),
                ('pathology', models.CharField(blank=True, max_length=25, null=True)),
                ('region', models.CharField(blank=True, max_length=25, null=True)),
                ('loq', models.FloatField(blank=True, null=True)),
                ('normalization_factor', models.FloatField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=3857)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.category', verbose_name='category of data')),
            ],
            options={
                'verbose_name': 'sample annotation',
                'verbose_name_plural': 'sample annotations',
                'ordering': ['roi_label'],
            },
        ),
        migrations.CreateModel(
            name='Cell_Types_for_Spatial_Decon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cluster_id', models.CharField(blank=True, max_length=8, null=True)),
                ('alias', models.CharField(blank=True, max_length=8, null=True)),
                ('data_set', models.CharField(blank=True, max_length=250, null=True)),
                ('number_of_cells', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('cell_type1', models.CharField(blank=True, max_length=125, null=True)),
                ('cell_type2', models.CharField(blank=True, max_length=125, null=True)),
                ('cell_type3', models.CharField(blank=True, max_length=125, null=True)),
                ('cell_type_specific', models.CharField(blank=True, max_length=125, null=True)),
                ('cell_type_general', models.CharField(blank=True, max_length=125, null=True)),
                ('cluster_name', models.CharField(blank=True, max_length=125, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.category', verbose_name='category of data')),
            ],
            options={
                'verbose_name': 'cell type',
                'verbose_name_plural': 'cell annotations (cell types)',
                'ordering': ['-number_of_cells', 'cluster_id'],
            },
        ),
    ]
