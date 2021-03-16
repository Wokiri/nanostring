import csv, io
from bokeh.models.layouts import Column, Spacer
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib  import messages
from django.contrib.gis.db.models import Q
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
    )

from .forms import (
    UploadCellTypesForm,
    SearchCellTypesForm,
    UpdateCellsTypeCSVsForm,
    )

all_cell_types = Cell_Types_for_Spatial_Decon.objects.all()



def home_page_view(request):
    template_name = 'pages/homepage.html'

    context = {
        'page_name': 'Home',
        'cell_types': all_cell_types[0:3],
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



def update_cell_type_view(request, clusterid):
    template_name = 'pages/update_cell_type.html'

    cell_type = get_object_or_404(Cell_Types_for_Spatial_Decon, cluster_id=clusterid)
    update_cells_type_csv_form = UpdateCellsTypeCSVsForm(instance=cell_type)

    if request.method == 'POST':
        update_cells_type_csv_form = UpdateCellsTypeCSVsForm(request.POST)
        if update_cells_type_csv_form.is_valid():
            Cell_Types_for_Spatial_Decon.objects.filter(cluster_id=clusterid).delete()
            cd_celltype = update_cells_type_csv_form.cleaned_data
            update_cells_type_csv_form.save()
            messages.success(request, f'Cell Type {cd_celltype["cluster_id"]} successfully updated.')
            return redirect('pages:messages_page', 'update-cell-type')

    context = {
        'page_name': f'Update {cell_type.cluster_id}',
        'update_cells_type_csv_form': update_cells_type_csv_form,
        'cell_type': cell_type,
    }

    return render(request, template_name, context)


def cell_types_for_spatial_decon_uploader_view(request):
    template_name = 'pages/files_upload.html'
    cell_types_form = UploadCellTypesForm()

    if request.method == 'POST':
        cell_types_form = UploadCellTypesForm(request.POST, request.FILES)
        if cell_types_form.is_valid:
            uploaded_file = request.FILES['file']

            # check if its csv
            if not uploaded_file.name.endswith('.csv'):
                messages.error(request, 'Uploaded file is not a csv!')
                return redirect('pages:messages_page')

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
            return redirect('pages:messages_page', 'file-upload')


    

    context = {
        'page_name': 'Upload cell_types csv File',
        'cell_types_form': cell_types_form
    }

    return render(request, template_name, context)




def cell_types_detail_view(request):
    template_name = 'pages/cell_types_analysis.html'

    cell_types = Cell_Types_for_Spatial_Decon.objects.order_by('-number_of_cells')

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
        search_value = cd['search_cell_type']
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
        'page_name': 'Cell Types Detail',
        'cell_types': cell_types,
        'search_cell_types_form': search_cell_types_form,
        'cells_type_describe_object': cells_type_describe_object,
        'script1': script1,
        'div1': div1,
        'script2': script2,
        'div2': div2,
    }

    return render(request, template_name, context)

