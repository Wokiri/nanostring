import csv, io
from django.shortcuts import render, redirect
from django.contrib  import messages
from django.contrib.gis.db.models import Q
from django.db import connection

# from bokeh.plotting import figure, output_file, show
# from bokeh.embed import components


from pandas import DataFrame
import pandas


from data.models import (
    Cell_Types_for_Spatial_Decon,
    )

from .forms import (
    UploadCellTypesForm,
    SearchCellTypesForm,
    )

all_cell_types = Cell_Types_for_Spatial_Decon.objects.all()



def home_page_view(request):
    template_name = 'pages/homepage.html'

    context = {
        'page_name': 'Home',
        'cell_types': all_cell_types[0:2],
    }

    return render(request, template_name, context)


def messages_view(request, prev_name):
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
                    clusterID = col[1],
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
    template_name = 'pages/cell_types_detail.html'

    from bokeh.plotting import figure
    from bokeh.embed import components

    cell_types = Cell_Types_for_Spatial_Decon.objects.order_by('clusterID')

    # cells_type_data = pandas.read_sql_query('''
    #     SELECT * FROM data_cell_types_for_spatial_decon
    #     ''',
    #     connection)

    cells_type_data = pandas.read_sql_query(
        str(Cell_Types_for_Spatial_Decon.objects.all().query),
        connection
        )



    search_cell_types_form = SearchCellTypesForm(request.GET or None)
    if search_cell_types_form.is_valid():
        cd = search_cell_types_form.cleaned_data
        search_value = cd['search_cell_type']
        cell_types = Cell_Types_for_Spatial_Decon.objects.filter(
            Q(clusterID__icontains=search_value)|
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

        if cell_types.count() == 0:
            messages.error(request, f'No Cell Types matches: "{search_value}".')
            return redirect('pages:messages_page', 'cell-types')

        # cells_type_data12 = pandas.read_sql_query(str(cell_types.query), connection)
        # print(cells_type_data12)


    cells_type_DF1 = DataFrame(cells_type_data, columns=['clusterID', 'number_of_cells'])

    clusterID = cells_type_DF1['clusterID']
    clusterID_list = []
    for item in clusterID:
        clusterID_list.append(item)

    number_of_cells = cells_type_DF1['number_of_cells']
    number_of_cells_list = []
    for item in number_of_cells:
        number_of_cells_list.append(item)
    

    # fig1: Bar Graph showing the Number of Cells against Cell ClusterID
    fig1=figure(
        title="Bar Graph showing the Number of Cells against Cell ClusterID",
        x_axis_label='Cell ClusterID',
        y_axis_label='Number of Cells',
        x_range=sorted(clusterID_list),
        plot_width=1200,
        plot_height=360,
        )
    fig1.title.align = "center"
    fig1.title.text_color = "darkgreen"
    fig1.title.text_font_size = "18px"
    fig1.vbar(x=clusterID_list, top=number_of_cells_list, width=0.5)

    # fig2: Pie Chart showing Cells Types categories by Dataset
    fig2 = figure(
        title="Pie Chart showing Cells Types categories by Dataset",
        # plot_width=250,
        plot_height=400
        )
    fig2.vbar(x=[1,2,3], width=0.5, bottom=0, top=[2,4,6], color="Red")

    script, div1 = components(fig1)
    script2, div2 = components(fig2)

    context = {
        'page_name': 'Cell Types Detail',
        'cell_types': cell_types,
        'search_cell_types_form': search_cell_types_form,
        'script': script,
        'div1': div1,
        'script2': script2,
        'div2': div2,
        # 'cells_type_df': somedata,
    }

    return render(request, template_name, context)

