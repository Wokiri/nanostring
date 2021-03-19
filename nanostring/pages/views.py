import csv, io
from bokeh.models.layouts import Column, Spacer
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib  import messages
from django.contrib.gis.db.models import Q
from django.contrib.gis.geos import Point
from django.db import connection
from django.views.generic import ListView

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
from bokeh.palettes import Category10_10, Greens256


from data.models import (
    Cell_Types_for_Spatial_Decon,
    Kidney_Sample_Annotations,
    )

from .forms import (
    UploadCellTypesForm,
    SearchCellTypesForm,
    UpdateCellsTypeCSVsForm,
    UploadSampleAnnotationsForm,
    update_sample_annotations_csv_form,
    SearchSampleAnnotationsForm,
    )

all_cell_types = Cell_Types_for_Spatial_Decon.objects.all()
all_sample_annotations_types = Kidney_Sample_Annotations.objects.all()



def home_page_view(request):
    template_name = 'pages/homepage.html'

    context = {
        'page_name': 'Home',
        'cell_types': all_cell_types[0:3],
        'sample_annotations': all_sample_annotations_types[0:3],
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



class CellTypeList(ListView):
    model = Cell_Types_for_Spatial_Decon


class SampleAnnotationList(ListView):
    model = Kidney_Sample_Annotations



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
                _, created = Kidney_Sample_Annotations.objects.update_or_create(
                    slide_name = col[1],
                    scan_name = col[2],
                    roi_label = col[3],
                    segment_label = col[4],
                    segment_display_name = col[5],
                    sample_id = col[6],
                    aoi_surface_area = col[7],
                    aoi_nuclei_count = col[8],
                    roi_coordinate_x = col[9],
                    roi_coordinate_y = col[10],
                    raw_reads = col[11],
                    trimmed_reads = col[12],
                    stitched_reads = col[13],
                    aligned_reads = col[14],
                    duplicated_reads = col[15],
                    sequencing_saturation = col[16],
                    umiq_30 = col[17],
                    rtsq_30 = col[18],
                    disease_status = col[19],
                    pathology = col[20],
                    region = col[21],
                    loq = col[22],
                    normalization_factor = col[23],
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


def update_sample_annotations_view(request, slug_value):
    template_name = 'pages/update_sample_annotations.html'

    sample_annotation = get_object_or_404(Kidney_Sample_Annotations, slug=slug_value)
    update_sample_annotations_form = update_sample_annotations_csv_form(instance=sample_annotation)

    if request.method == 'POST':
        update_sample_annotations_form = update_sample_annotations_csv_form(request.POST)
        if update_sample_annotations_form.is_valid():
            cd = update_sample_annotations_form.cleaned_data
            Kidney_Sample_Annotations.objects.filter(slug=slug_value).update(**cd)
            messages.success(request, f'Sample Annotation {cd["slug_value"]} successfully updated.')
            return redirect('pages:messages_page', 'update-sample-annotation')

    context = {
        'page_name': f'Update {sample_annotation.slug}',
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
                _, created = Cell_Types_for_Spatial_Decon.objects.update_or_create(
                    cluster_id = col[1],
                    alias = col[2],
                    data_set = col[3],
                    number_of_cells = col[4],
                    cell_type1 = col[5],
                    cell_type2 = col[6],
                    cell_type3 = col[7],
                    cell_type_specific = col[8],
                    cell_type_general = col[9],
                    cluster_name = col[10],
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
    update_cells_type_csv_form = UpdateCellsTypeCSVsForm(instance=cell_type)

    if request.method == 'POST':
        update_cells_type_csv_form = UpdateCellsTypeCSVsForm(request.POST)
        if update_cells_type_csv_form.is_valid():
            cd_celltype = update_cells_type_csv_form.cleaned_data
            Cell_Types_for_Spatial_Decon.objects.filter(cluster_id=clusterid).update(**cd_celltype)
            messages.success(request, f'Cell Type {cd_celltype["cluster_id"]} successfully updated.')
            return redirect('pages:messages_page', 'update-cell-type')

    context = {
        'page_name': f'Update {cell_type.cluster_id}',
        'update_cells_type_csv_form': update_cells_type_csv_form,
        'cell_type': cell_type,
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


def sample_annotations_analysis_view(request):
    template_name = 'pages/sample_annotation_analysis.html'
    sample_annotations = Kidney_Sample_Annotations.objects.all()
    search_count = sample_annotations.count()

    sample_annotations_search_form = SearchSampleAnnotationsForm(request.GET or None)
    if sample_annotations_search_form.is_valid():
        cd = sample_annotations_search_form.cleaned_data
        search_value = cd['search_value']
        sample_annotations = Kidney_Sample_Annotations.objects.filter(
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

        if sample_annotations.count() == 0:
            messages.error(request, f'No Sample Annotations matches: "{search_value}".')
            return redirect('pages:messages_page', 'sample-annotations-analysis')
        else:
            search_count = sample_annotations.count()


    context = {
        'page_name': 'Sample Annotations Analysis',
        'sample_annotations': sample_annotations,
        'sample_annotations_search_form': sample_annotations_search_form,
        'search_count': search_count,
    }
    return render(request, template_name, context)