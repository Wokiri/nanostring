
from django.urls import path

from .views import (
    home_page_view,
    about_page_view,
    foss_licenses_page_view,
    cell_types_for_spatial_decon_uploader_view,
    cell_types_analysis_view,
    CellTypeList,
    SampleAnnotationList,
    update_cell_type_view,
    update_sample_annotations_view,
    messages_view,
    kidney_sample_annotations_uploader_view,
    sample_annotations_analysis_view,
    feature_annotation_analysis_view,
    upload_csvs_view,
    kidney_raw_bioProbeCountMatrix_analysis_view,
    KidneyRawTargetCountMatrix_analysis_view,
    KidneyQ3NormTargetCountMatrix_analysis_view,
    kidneyssGSEA_analysis_view,
    average_gene_expression_analysis_view,
)

app_name = 'pages'

urlpatterns = [
    path('', home_page_view, name='home_page'),
    path('about-us/', about_page_view, name='about_page'),
    path('foss-licenses/', foss_licenses_page_view, name='foss_licenses_page'),
    path('celltype-upload/', cell_types_for_spatial_decon_uploader_view, name='upload_celltype_page'),
    path('sampleannotation-upload/', kidney_sample_annotations_uploader_view, name='upload_sampleannotation_page'),
    path('cell-types-analysis/', cell_types_analysis_view, name='cell-types-analysis_page'),
    path('sample-annotations-analysis/', sample_annotations_analysis_view, name='sample_annotations_analysis_page'),
    path('messages/', messages_view, name='messages_page'),
    path('<slug:prev_name>/messages/', messages_view, name='messages_page'),
    path('cell-type-list/', CellTypeList.as_view(), name='list_cell_type_page'),
    path('update-cell-type/<slug:clusterid>/', update_cell_type_view, name='update_cell_type_page'),
    path('sample-annotation-list/', SampleAnnotationList.as_view(), name='list_sample_annotation_page'),
    path('update-sample-annotation/<int:id_value>/', update_sample_annotations_view, name='update_sample_annotation_page'),
    path('feature-annotations-analysis/', feature_annotation_analysis_view, name='feature_annotations_analysis_page'),
    path('upload-csvs/', upload_csvs_view, name='upload_csvs_page'),
    path('probe-expression-analysis/', kidney_raw_bioProbeCountMatrix_analysis_view, name='probe_expression_analysis_page'),
    path('target-expression-analysis/', KidneyRawTargetCountMatrix_analysis_view, name='target_expression_analysis_page'),
    path('normalized-expression-analysis/', KidneyQ3NormTargetCountMatrix_analysis_view, name='normalized_expression_analysis_page'),
    path('kidneyssGSEA-analysis/', kidneyssGSEA_analysis_view, name='kidneyssGSEA_analysis_page'),
    path('average-gene-expression-analysis/', average_gene_expression_analysis_view, name='average_gene_expression_analysis_page'),


]
