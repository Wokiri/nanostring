"""nanostring URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from .views import (
    home_page_view,
    about_page_view,
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
    feature_annotation_uploader_view,
    update_feature_annotation_view,
    FeatureAnnotationList,
)

app_name = 'pages'

urlpatterns = [
    path('', home_page_view, name='home_page'),
    path('about-us/', about_page_view, name='about_page'),
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
    path('featureannotation-upload/', feature_annotation_uploader_view, name='upload_featureannotation_page'),
    path('update-feature-annotation/<slug:rts_id>/', update_feature_annotation_view, name='update_feature_annotation_page'),
    path('feature-annotation-list/', FeatureAnnotationList.as_view(), name='list_feature_annotation_page'),

]
