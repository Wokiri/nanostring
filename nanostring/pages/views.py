import csv, io
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.contrib  import messages
from django.contrib.gis.db.models import Q
from django.contrib.gis.geos import Point
from django.db import connection
from django.views.generic import ListView
from django.core.serializers import serialize

from math import pi, floor


from pandas import DataFrame
import pandas

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import (
    ColumnDataSource, 
    DataTable, 
    TableColumn,
    )
from bokeh.transform import cumsum
from bokeh.layouts import Column
from bokeh.palettes import Category10_10, Category10_3, Greens256, Category10
from bokeh.models.layouts import Column, Spacer



from data.models import (
    Cell_Types_for_Spatial_Decon,
    Kidney_Sample_Annotations,
    Kidney_Feature_Annotation,
    )

from .forms import (
    UploadCellTypesForm,
    SearchCellTypesForm,
    UpdateCellsTypeCSVsForm,
    UploadSampleAnnotationsForm,
    UpdateSampleAnnotationsCSVForm,
    SearchSampleAnnotationsForm,
    UploadFeatureAnnotationsForm,
    UpdateFeatureAnnotationForm,
    SearchFeatureAnnotationsForm,
    )

all_cell_types = Cell_Types_for_Spatial_Decon.objects.all()
all_sample_annotations_types = Kidney_Sample_Annotations.objects.all()
all_kidney_feature_annotations = Kidney_Feature_Annotation.objects.all()



def home_page_view(request):
    template_name = 'pages/homepage.html'

    context = {
        'page_name': 'Home',
        'cell_types': all_cell_types[0:3],
        'sample_annotations': all_sample_annotations_types[0:3],
        'kidney_feature_annotations': all_kidney_feature_annotations[0:3],
    }

    return render(request, template_name, context)


def messages_view(request, prev_name=None):
    template_name = 'pages/messages.html'

    context = {
        'page_name': 'Messages',
    }

    return render(request, template_name, context)



def about_page_view(request):
    template_name = 'pages/about_nanostring.html'

    context = {
        'page_name': 'About',
    }

    return render(request, template_name, context)


class SampleAnnotationList(ListView):
    model = Kidney_Sample_Annotations
    paginate_by = 60


class CellTypeList(ListView):
    model = Cell_Types_for_Spatial_Decon

class FeatureAnnotationList(ListView):
    model = Kidney_Feature_Annotation
    paginate_by = 100


def kidney_sample_annotations_uploader_view(request):
    template_name = 'pages/sampleannotation_upload.html'
    sample_annotations_form = UploadSampleAnnotationsForm()

    if request.method == 'POST':
        sample_annotations_form = UploadSampleAnnotationsForm(request.POST, request.FILES)
        if sample_annotations_form.is_valid:
            uploaded_file = request.FILES['file']

            # check if its csv
            if not uploaded_file.name.endswith('.csv'):
                messages.error(request, 'Uploaded file is not a csv!')
                return redirect('pages:messages_page', 'sampleannotation-upload')

            # check if its the right csv
            if uploaded_file.name != 'Kidney_Sample_Annotations.csv':
                messages.error(request, '''Uploaded file is not the right csv!\n
                    Ensure it is: Kidney_Sample_Annotations.csv''')
                return redirect('pages:messages_page', 'sampleannotation-upload')


            # If its csv
            file_data = uploaded_file.read().decode('UTF-8')

            # Set up stream
            io_string = io.StringIO(file_data)
            next(io_string) # Skips the header row
            for col in csv.reader(io_string, delimiter=','):
                new_sample_annotation, created = Kidney_Sample_Annotations.objects.update_or_create(
                    segment_display_name = col[5],
                    defaults = {
                        'slide_name' : col[1],
                        'scan_name' : col[2],
                        'roi_label' : col[3],
                        'segment_label' : col[4],
                        'segment_display_name' : col[5],
                        'sample_id' : col[6],
                        'aoi_surface_area' : col[7],
                        'aoi_nuclei_count' : col[8],
                        'roi_coordinate_x' : col[9],
                        'roi_coordinate_y' : col[10],
                        'raw_reads' : col[11],
                        'trimmed_reads' : col[12],
                        'stitched_reads' : col[13],
                        'aligned_reads' : col[14],
                        'duplicated_reads' : col[15],
                        'sequencing_saturation' : col[16],
                        'umiq_30' : col[17],
                        'rtsq_30' : col[18],
                        'disease_status' : col[19],
                        'pathology' : col[20],
                        'region' : col[21],
                        'loq' : col[22],
                        'normalization_factor' : col[23]
                    }
                )
            for cell in Kidney_Sample_Annotations.objects.all():
                cell.geom = (Point(cell.roi_coordinate_x, cell.roi_coordinate_y))
                cell.save()
            messages.success(request,'File data successfully written to the Database.')
            return redirect('pages:messages_page', 'sampleannotation-upload')


    context = {
        'page_name': 'Upload Sample Annotations file',
        'sample_annotations_form': sample_annotations_form
    }

    return render(request, template_name, context)


def update_sample_annotations_view(request, id_value):
    template_name = 'pages/update_sample_annotations.html'

    sample_annotation = get_object_or_404(Kidney_Sample_Annotations, id=id_value)
    update_sample_annotations_form = UpdateSampleAnnotationsCSVForm(request.POST or None, instance=sample_annotation)
    if update_sample_annotations_form.is_valid():
        update_sample_annotations_form.save()
        messages.success(request, f'Sample Annotation {sample_annotation.segment_display_name} successfully updated.')
        return redirect('pages:messages_page', 'sample-annotation-list')

    context = {
        'page_name': f'Update {sample_annotation.segment_display_name}',
        'update_sample_annotations_form': update_sample_annotations_form,
        'sample_annotation': sample_annotation,
    }

    return render(request, template_name, context)



def cell_types_for_spatial_decon_uploader_view(request):
    template_name = 'pages/celltype_upload.html'
    cell_types_form = UploadCellTypesForm()

    if request.method == 'POST':
        cell_types_form = UploadCellTypesForm(request.POST, request.FILES)
        if cell_types_form.is_valid:
            uploaded_file = request.FILES['file']

            # check if its csv
            if not uploaded_file.name.endswith('.csv'):
                messages.error(request, 'Uploaded file is not a csv!')
                return redirect('pages:messages_page', 'celltype-upload')

            # check if its the right csv
            if uploaded_file.name != 'Cell_Types_for_Spatial_Decon.csv':
                messages.error(request, '''Uploaded file is not the right csv!
                    \nEnsure it is: Cell_Types_for_Spatial_Decon.csv''')
                return redirect('pages:messages_page', 'celltype-upload')

            # If its csv
            file_data = uploaded_file.read().decode('UTF-8')

            # Set up stream
            io_string = io.StringIO(file_data)
            next(io_string) # Skips the header row
            for col in csv.reader(io_string, delimiter=','):
                new_cell_type, created = Cell_Types_for_Spatial_Decon.objects.update_or_create(
                    cluster_id= col[1],
                    defaults={
                        'cluster_id' : col[1],
                        'alias' : col[2],
                        'data_set' : col[3],
                        'number_of_cells' : col[4],
                        'cell_type1' : col[5],
                        'cell_type2' : col[6],
                        'cell_type3' : col[7],
                        'cell_type_specific' : col[8],
                        'cell_type_general' : col[9],
                        'cluster_name' : col[10],
                    }
                )
            messages.success(request,'File data successfully written to the Database.')
            return redirect('pages:messages_page', 'celltype-upload')


    

    context = {
        'page_name': 'Upload Cell Types file',
        'cell_types_form': cell_types_form
    }

    return render(request, template_name, context)



def update_cell_type_view(request, clusterid):
    template_name = 'pages/update_cell_type.html'

    cell_type = get_object_or_404(Cell_Types_for_Spatial_Decon, cluster_id=clusterid)
    update_cells_type_csv_form = UpdateCellsTypeCSVsForm(request.POST or None, instance=cell_type)
    if update_cells_type_csv_form.is_valid():
        update_cells_type_csv_form.save()
        messages.success(request, f'Cell Type {cell_type.cluster_id} successfully updated.')
        return redirect('pages:messages_page', 'cell-type-list')

    context = {
        'page_name': f'Update {cell_type.cluster_id}',
        'update_cells_type_csv_form': update_cells_type_csv_form,
        'cell_type': cell_type,
    }

    return render(request, template_name, context)



def sample_annotations_analysis_view(request):
    template_name = 'pages/sample_annotation_analysis.html'
    sample_annotations = Kidney_Sample_Annotations.objects.all()
    search_count = sample_annotations.count()

    sample_annotations_data = pandas.read_sql_query(
        str(Kidney_Sample_Annotations.objects.all().query),
        connection
        )

    sample_annotations_DF = DataFrame(sample_annotations_data, columns=['disease_status', 'segment_display_name'])
    
    sample_annotations_search_form = SearchSampleAnnotationsForm(request.GET or None)
    if sample_annotations_search_form.is_valid():
        cd = sample_annotations_search_form.cleaned_data
        search_value = cd['search_value']
        sample_annotations = Kidney_Sample_Annotations.objects.filter(
            Q(id__icontains=search_value) |
            Q(slide_name__icontains=search_value) |
            Q(scan_name__icontains=search_value) |
            Q(roi_label__icontains=search_value) |
            Q(segment_label__icontains=search_value) |
            Q(segment_display_name__icontains=search_value) |
            Q(sample_id__icontains=search_value) |
            Q(aoi_surface_area__icontains=search_value) |
            Q(aoi_nuclei_count__icontains=search_value) |
            Q(roi_coordinate_x__icontains=search_value) |
            Q(roi_coordinate_y__icontains=search_value) |
            Q(raw_reads__icontains=search_value) |
            Q(trimmed_reads__icontains=search_value) |
            Q(stitched_reads__icontains=search_value) |
            Q(aligned_reads__icontains=search_value) |
            Q(duplicated_reads__icontains=search_value) |
            Q(sequencing_saturation__icontains=search_value) |
            Q(umiq_30__icontains=search_value) |
            Q(rtsq_30__icontains=search_value) |
            Q(disease_status__icontains=search_value) |
            Q(pathology__icontains=search_value) |
            Q(region__icontains=search_value) |
            Q(loq__icontains=search_value) |
            Q(normalization_factor__icontains=search_value)
        )

        sql_search_query = '''
        SELECT * FROM data_kidney_sample_annotations WHERE
        CAST (id AS TEXT) ILIKE %(search_value)s OR
        slide_name ILIKE %(search_value)s OR
        scan_name ILIKE %(search_value)s OR
        CAST (roi_label AS TEXT) ILIKE %(search_value)s OR
        segment_label ILIKE %(search_value)s OR
        segment_display_name ILIKE %(search_value)s OR
        sample_id ILIKE %(search_value)s OR
        CAST (aoi_surface_area AS TEXT) ILIKE %(search_value)s OR
        CAST (aoi_nuclei_count AS TEXT) ILIKE %(search_value)s OR
        CAST (roi_coordinate_x AS TEXT) ILIKE %(search_value)s OR
        CAST (roi_coordinate_y AS TEXT) ILIKE %(search_value)s OR
        CAST (raw_reads AS TEXT) ILIKE %(search_value)s OR
        CAST (trimmed_reads AS TEXT) ILIKE %(search_value)s OR
        CAST (stitched_reads AS TEXT) ILIKE %(search_value)s OR
        CAST (aligned_reads AS TEXT) ILIKE %(search_value)s OR
        CAST (duplicated_reads AS TEXT) ILIKE %(search_value)s OR
        CAST (sequencing_saturation AS TEXT) ILIKE %(search_value)s OR
        CAST (umiq_30 AS TEXT) ILIKE %(search_value)s OR
        CAST (rtsq_30 AS TEXT) ILIKE %(search_value)s OR
        disease_status ILIKE %(search_value)s OR
        pathology ILIKE %(search_value)s OR
        region ILIKE %(search_value)s OR
        CAST (loq AS TEXT) ILIKE %(search_value)s OR
        CAST (normalization_factor AS TEXT) ILIKE %(search_value)s
        '''

        sample_annotations_data = pandas.read_sql_query(sql_search_query, connection, params={'search_value':f'%{search_value}%'})
        sample_annotations_DF = DataFrame(sample_annotations_data, columns=['disease_status', 'segment_display_name'])

        if sample_annotations.count() == 0:
            messages.error(request, f'No Sample Annotations matches: "{search_value}".')
            return redirect('pages:messages_page', 'sample-annotations-analysis')
        else:
            search_count = sample_annotations.count()


    sample_annotations_vector_geoson = serialize(
        'geojson',
        sample_annotations,
        geometry_field='geom',
        fields=('disease_status','segment_display_name')
        )
    all_lons = [float(i.geom[0]) for i in sample_annotations]
    all_lats = [float(i.geom[1]) for i in sample_annotations]

    map_lon = float(sum(all_lons)/len(all_lons))
    map_lat = float(sum(all_lats)/len(all_lats))
    map_zoom = float(40)

    disease_status_group = sample_annotations_DF.groupby(['disease_status']).count()

    # Create value column to be used for piechart angles
    disease_status_group['value'] = (
        disease_status_group['segment_display_name']/len(sample_annotations_DF) * 2*pi
        )
    disease_status_group['proportion'] = (
        disease_status_group['segment_display_name']
        )
    disease_status_group['color'] = ['orangered', 'mediumblue'][:len(disease_status_group)]
    
    disease_status_groups_CDS = ColumnDataSource(disease_status_group)


    sample_annotations_tooltips= [
            ('Disease Status', '@disease_status'),
            ('Proportion', f'@proportion out of {len(sample_annotations_DF)}'),
        ]

    sample_annotations_fig=figure(
        title="Pie Chart showing Kidney Sample Annotations categorized by Disease Status",
        plot_height=600,
        plot_width=992,
        tooltips=sample_annotations_tooltips,
        )

    sample_annotations_fig.wedge(
        x=0,
        y=1,
        radius=0.45,
        start_angle=cumsum('value', include_zero=True),
        end_angle=cumsum('value'),
        line_color="white",
        fill_color='color',
        source=disease_status_groups_CDS,
        legend_field='disease_status',
        )

    sample_annotations_fig.axis.visible=False
    sample_annotations_fig.axis.axis_line_color=None
    sample_annotations_fig.toolbar.active_drag = None
    sample_annotations_fig.title.align = "center"
    sample_annotations_fig.title.text_color = "DarkSlateBlue"
    sample_annotations_fig.title.text_font_size = "18px"
    sample_annotations_fig.legend.orientation = "vertical"
    sample_annotations_fig.legend.location = "right"
    
    script, div = components(sample_annotations_fig)
    
    context = {
        'page_name': 'Sample Annotations Analysis',
        'sample_annotations': sample_annotations,
        'sample_annotations_search_form': sample_annotations_search_form,
        'search_count': search_count,
        'sample_annotations_vector_geoson': sample_annotations_vector_geoson,
        'map_lon': map_lon,
        'map_lat': map_lat,
        'map_zoom': map_zoom,
        'script': script,
        'div': div,
    }
    return render(request, template_name, context)



def cell_types_analysis_view(request):
    template_name = 'pages/cell_types_analysis.html'
    cell_types = Cell_Types_for_Spatial_Decon.objects.order_by('-number_of_cells')
    search_count = cell_types.count()


    # cells_type_data = pandas.read_sql_query('''
    #     SELECT * FROM data_cell_types_for_spatial_decon
    #     ''',
    #     connection)

    cells_type_data = pandas.read_sql_query(
        str(Cell_Types_for_Spatial_Decon.objects.all().query),
        connection
        )

    DF_columns=[
        'cluster_id',
        'number_of_cells',
        'alias',
        'data_set',
        'cell_type_specific',
        'cell_type_general',
        ]

    cells_type_DF = DataFrame(cells_type_data, columns=DF_columns)
    

    search_cell_types_form = SearchCellTypesForm(request.GET or None)
    if search_cell_types_form.is_valid():
        cd = search_cell_types_form.cleaned_data
        search_value = cd['search_value']
        cell_types = Cell_Types_for_Spatial_Decon.objects.filter(
            Q(cluster_id__icontains=search_value)|
            Q(alias__icontains=search_value) |
            Q(data_set__icontains=search_value) |
            Q(number_of_cells__icontains=search_value) |
            Q(cell_type1__icontains=search_value) |
            Q(cell_type2__icontains=search_value) |
            Q(cell_type3__icontains=search_value) |
            Q(cell_type_specific__icontains=search_value) |
            Q(cell_type_general__icontains=search_value) |
            Q(cluster_name__icontains=search_value)
            )

        sql_search_query = '''
        SELECT * FROM data_cell_types_for_spatial_decon WHERE
        cluster_id ILIKE %(search_value)s OR
        alias ILIKE %(search_value)s OR
        data_set ILIKE %(search_value)s OR
        CAST (number_of_cells AS TEXT) ILIKE %(search_value)s OR
        cell_type1 ILIKE %(search_value)s OR
        cell_type2 ILIKE %(search_value)s OR
        cell_type3 ILIKE %(search_value)s OR
        cell_type_specific ILIKE %(search_value)s OR
        cell_type_general ILIKE %(search_value)s OR
        cluster_name ILIKE %(search_value)s
        '''
        search_cells_type_data = pandas.read_sql_query(sql_search_query, connection, params={'search_value':f'%{search_value}%'})
        cells_type_DF = DataFrame(search_cells_type_data, columns=DF_columns)

        if cell_types.count() == 0:
            messages.error(request, f'No Cell Types matches: "{search_value}".')
            return redirect('pages:messages_page', 'cell-types')
        else:
            search_count = cell_types.count()


    cluster_id = cells_type_DF['cluster_id']
    number_of_cells = cells_type_DF['number_of_cells']
    cells_type_DF['bar_color'] = sorted(
        [Greens256[floor(item)] for item in cells_type_DF['number_of_cells']/cells_type_DF['number_of_cells'].sum() * 255],
        reverse=False
        )
        
    
    cluster_id_list = []
    for item in cluster_id:
        cluster_id_list.append(item)
        

    number_of_cells_list = []
    for item in number_of_cells:
        number_of_cells_list.append(item)
        

    cells_type_describe_values = []
    for item in cells_type_DF.describe()['number_of_cells']:
        cells_type_describe_values.append(item)
        
    cells_type_describe_object = {
        'count': cells_type_describe_values[0],
        'mean': cells_type_describe_values[1],
        'std': cells_type_describe_values[2],
        'min': cells_type_describe_values[3],
        '25': cells_type_describe_values[4],
        '50': cells_type_describe_values[5],
        '75': cells_type_describe_values[6],
        'max': cells_type_describe_values[7],
    }
    
    cells_type_CDS_bar = ColumnDataSource(cells_type_DF)

    # fig1: Bar Graph showing the Number of Cells against Cell cluster_id
    fig1_tooltips= [
            ('Cluster ID', '@cluster_id'),
            ('Number of Cells', '@number_of_cells'),
            ('Specific Cell Type', '@cell_type_specific'),
            ('General Cell Type', '@cell_type_general'),
        ]
    fig1=figure(
        title="Bar Graph showing Number of Cells against Cell clusterID",
        x_axis_label='Cell clusterID',
        y_axis_label='Number of Cells',
        x_range=sorted(cluster_id_list, key=lambda x: number_of_cells_list[cluster_id_list.index(x)], reverse=True),
        plot_width=1200,
        plot_height=500,
        tooltips=fig1_tooltips,
        toolbar_location='below',
        )
        
    fig1.toolbar.active_drag = None
    fig1.title.align = "center"
    fig1.title.text_color = "darkgreen"
    fig1.title.text_font_size = "18px"
    fig1.xaxis.major_label_text_color = 'darkgreen'
    fig1.yaxis.major_label_text_color = 'darkgreen'
    fig1.xgrid.grid_line_color = None
    fig1.y_range.start=0
    fig1.vbar(
        x='cluster_id',
        top='number_of_cells',
        source=cells_type_CDS_bar,
        width=0.8,
        fill_color='bar_color',
        line_color ='midnightblue',
        )
    script1, div1 = components(fig1)



    data_set_groups_sum = cells_type_DF.groupby(['data_set']).sum()
    data_set_groups_sum['value'] = (
        data_set_groups_sum['number_of_cells']/data_set_groups_sum['number_of_cells'].sum() * 2*pi
        )
    data_set_groups_sum['value_weight'] = (
        data_set_groups_sum['number_of_cells']/data_set_groups_sum['number_of_cells'].sum() * 100
        )
    data_set_groups_sum['color'] = Category10_10[:len(data_set_groups_sum)]
    cells_data_set_groups_CDS = ColumnDataSource(data_set_groups_sum)
    

    fig2_tooltips= [
            ('Data set', '@data_set'),
            ('Number of cells', '@number_of_cells'),
            ('Percentage of total cells', '@value_weight'),
        ]

    fig2=figure(
        title="Pie Chart showing grouped Data_Sets weighted by aggregate Number of Cells",
        plot_height=600,
        plot_width=992,
        tooltips=fig2_tooltips,
        # toolbar_location='below',
        
        )
    fig2.wedge(
        x=0,
        y=1,
        radius=0.45,
        start_angle=cumsum('value', include_zero=True),
        end_angle=cumsum('value'),
        line_color="greenyellow",
        fill_color='color',
        source=cells_data_set_groups_CDS,
        legend_field='data_set',
        )

    fig2.axis.visible=False
    fig2.axis.axis_line_color=None
    fig2.toolbar.active_drag = None
    fig2.title.align = "center"
    fig2.title.text_color = "DarkSlateBlue"
    fig2.title.text_font_size = "18px"
    fig2.legend.orientation = "horizontal"
    fig2.legend.location = "top_center"
    
    script2, div2 = components(fig2)
    
    context = {
        'page_name': 'Cell Types Analysis',
        'cell_types': cell_types,
        'search_cell_types_form': search_cell_types_form,
        'search_count': search_count,
        'cells_type_describe_object': cells_type_describe_object,
        'script1': script1,
        'div1': div1,
        'script2': script2,
        'div2': div2,
    }

    return render(request, template_name, context)


def feature_annotation_uploader_view(request):
    template_name = 'pages/featureannotation_upload.html'
    feature_annotation_upload_form = UploadFeatureAnnotationsForm()

    if request.method == 'POST':
        feature_annotation_upload_form = UploadCellTypesForm(request.POST, request.FILES)
        if feature_annotation_upload_form.is_valid:
            uploaded_file = request.FILES['file']

            # check if its csv
            if not uploaded_file.name.endswith('.csv'):
                messages.error(request, 'Uploaded file is not a csv!')
                return redirect('pages:messages_page', 'featureannotation-upload')

            # check if its the right csv
            if uploaded_file.name != 'Kidney_Feature_Annotations.csv':
                messages.error(request, '''Uploaded file is not the right csv!
                    \nEnsure it is: Kidney_Feature_Annotations.csv''')
                return redirect('pages:messages_page', 'featureannotation-upload')

            # If its csv
            file_data = uploaded_file.read().decode('UTF-8')

            # Set up stream
            io_string = io.StringIO(file_data)
            next(io_string) # Skips the header row
            for col in csv.reader(io_string, delimiter=','):
                new_data, created = Kidney_Feature_Annotation.objects.update_or_create(
                    rts_id= col[1],
                    defaults={
                        'rts_id' : col[1],
                        'target_name' : col[2],
                        'probe_id' : col[3],
                        'negative' : col[4],
                    }
                )
            messages.success(request,'File data successfully written to the Database.')
            return redirect('pages:messages_page', 'featureannotation-upload')

    context = {
        'page_name': 'Upload Feature Annotation file',
        'feature_annotation_upload_form': feature_annotation_upload_form
    }

    return render(request, template_name, context)



def update_feature_annotation_view(request, rts_id):
    template_name = 'pages/update_feature_annotation.html'

    feature_annotation = get_object_or_404(Kidney_Feature_Annotation, rts_id=rts_id)
    update_feature_annotation_form = UpdateFeatureAnnotationForm(request.POST or None, instance=feature_annotation)
    if update_feature_annotation_form.is_valid():
        update_feature_annotation_form.save()
        messages.success(request, f'Feature Annotation {feature_annotation.rts_id} successfully updated.')
        return redirect('pages:messages_page', 'feature-annotation-list')

    context = {
        'page_name': f'Update {feature_annotation.rts_id}',
        'update_feature_annotation_form': update_feature_annotation_form,
        'feature_annotation': feature_annotation,
    }

    return render(request, template_name, context)



def feature_annotation_analysis_view(request):
    template_name = 'pages/kidney_feature_annotations_analysis.html'
    kidney_feature_annotations = Kidney_Feature_Annotation.objects.order_by('rts_id')
    search_count = kidney_feature_annotations.count()

    feature_annotations_data = pandas.read_sql_query(
        str(Kidney_Feature_Annotation.objects.all().query),
        connection
        )

    DF_columns=[
        'rts_id',
        'negative',
        ]

    feature_annotations_DF = DataFrame(feature_annotations_data, columns=DF_columns)

    search_feature_annotations_form = SearchFeatureAnnotationsForm(request.GET or None)
    if search_feature_annotations_form.is_valid():
        cd = search_feature_annotations_form.cleaned_data
        search_value = cd['search_value']
        kidney_feature_annotations = Kidney_Feature_Annotation.objects.filter(
            Q(id__icontains=search_value) |
            Q(rts_id__icontains=search_value) |
            Q(target_name__icontains=search_value) |
            Q(probe_id__icontains=search_value) |
            Q(negative__icontains=search_value) 
        )

        sql_search_query = '''
        SELECT * FROM data_kidney_feature_annotation WHERE
        target_name ILIKE %(search_value)s OR
        rts_id ILIKE %(search_value)s OR
        CAST (id AS TEXT) ILIKE %(search_value)s OR
        CAST (probe_id AS TEXT) ILIKE %(search_value)s
        '''
        search_data = pandas.read_sql_query(sql_search_query, connection, params={'search_value':f'%{search_value}%'})
        feature_annotations_DF = DataFrame(search_data, columns=DF_columns)

        if kidney_feature_annotations.count() == 0:
            messages.error(request, f'No Feature Annotations matches: "{search_value}".')
            return redirect('pages:messages_page', 'feature-annotations-analysis')
        else:
            search_count = kidney_feature_annotations.count()


    group_by_negative = feature_annotations_DF.groupby(['negative']).count()

    # Create value column to be used for piechart angles
    group_by_negative['value'] = (
        group_by_negative['rts_id']/len(feature_annotations_DF) * 2*pi
        )
    group_by_negative['color'] = ['violet', 'Turquoise'][:len(group_by_negative)]
    group_by_negative_CDS = ColumnDataSource(group_by_negative)

    feature_annotations_tooltips= [
            ('Negative Status', '@negative'),
            ('Proportion', f'@rts_id out of {len(feature_annotations_DF)}'),
        ]


    pie=figure(
        title="Pie Chart showing Feature Annotation Proportions of Negative Records",
        plot_height=600,
        plot_width=992,
        tooltips=feature_annotations_tooltips
        )
    pie.wedge(
        x=0,
        y=1,
        radius=0.45,
        start_angle=cumsum('value', include_zero=True),
        end_angle=cumsum('value'),
        line_color="white",
        fill_color='color',
        source=group_by_negative_CDS,
        legend_field='negative',
    )
    pie.axis.visible=False
    pie.toolbar.active_drag = None
    pie.title.align = "center"
    pie.title.text_color = "RebeccaPurple"
    pie.title.text_font_size = "18px"
    pie.legend.orientation = "vertical"
    pie.legend.location = "right"

    script_pie, div_pie = components(pie)


    context = {
        'page_name': 'Feature Annotation Analysis',
        'kidney_feature_annotations': kidney_feature_annotations,
        'search_count': search_count,
        'search_feature_annotations_form': search_feature_annotations_form,
        'script_pie': script_pie,
        'div_pie': div_pie,
    }

    return render(request, template_name, context)
    