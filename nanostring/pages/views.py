import csv, io
from pathlib import Path, PurePath
import urllib
import json
from bokeh.core.property.instance import Instance



from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from django.core.paginator import Paginator
from django.contrib  import messages
from django.contrib.gis.db.models import Q
from django.contrib.gis.geos import Point
from django.contrib.gis.gdal import OGRGeometry
from django.db import connection
from django.views.generic import ListView
from django.core.serializers import serialize

from math import pi, floor


from pandas import DataFrame
import pandas

import bokeh
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import (
    ColumnDataSource,
    FactorRange,
    DataTable, 
    TableColumn,
    )
from bokeh.transform import cumsum
from bokeh.layouts import Column
from bokeh.palettes import Category10_10, PuRd3, Greens256, Category10
from bokeh.models.layouts import Column, Spacer



from .foss_licences import (
    bokeh_license,
    bootstrap_license,
    django_license,
    openlayers_license,
    python_license,
    qgis_license,
)


from data.models import (
    Category,
    Cell_Types_for_Spatial_Decon,
    Kidney_Sample_Annotations,
    RawCSVFiles,
    Disease2BScanVectorized,
    Normal2BScanVectorized,
    )

from .forms import (
    DownloadDataForm,
    CategoryModelForm,
    UploadCellTypesForm,
    SearchCellTypesForm,
    UpdateCellsTypeCSVsForm,
    UploadSampleAnnotationsForm,
    UpdateSampleAnnotationsCSVForm,
    SearchSampleAnnotationsForm,
    SearchFeatureAnnotationsForm,
    UploadRawCSVFilesModelForm,
    SearchProbeExpressionForm,
    QuantileSearchForm,
    SearchTargetExpressionForm,
    SearchNormalizedExpressionForm,
    SearchKidneyssGSEAForm,
    SearchAverageGeneExpressionForm,
    Disease2BScanVectorizedModelForm,
    Normal2BScanVectorizedModelForm,
    )

all_cell_types = Cell_Types_for_Spatial_Decon.objects.all()
all_sample_annotations_types = Kidney_Sample_Annotations.objects.all()
all_raw_csv_files = RawCSVFiles.objects.all()

from .handle_uploaded_files import (
    feature_annotations_DF,
    probe_expression_DF,
    target_expression_DF,
    normalized_expression_DF,
    ssGSEA_expression_DF,
    average_gene_expression_DF,
)


def download_data_view(request):
    template_name = 'pages/download_data.html'

    save_dir_path = PurePath(Path.home(), "Downloads",)

    def nanostringtextdata_tocsvdata(text_name):
        text_file = PurePath(save_dir_path, text_name)
        csv_name = text_name.replace('txt', 'csv')
        csv_file = PurePath(save_dir_path, csv_name)

        df = pandas.read_csv(text_file, delimiter=',')
        df.to_csv(csv_file)

        if Path(csv_file).exists:
            messages.success(request, f"CSV file {csv_file} is successfully created.")
            return redirect('pages:messages_page', 'download-data')
        else:
            messages.error(request, f"CSV file {csv_file} WAS NOT created.")
            return redirect('pages:messages_page', 'download-data')
    

    download_form = DownloadDataForm(request.GET or None)

    if download_form.is_valid() and 'data_name' in request.GET:
        cd = download_form.cleaned_data
        name_of_data = cd['data_name']
        
        save_data_path = PurePath(save_dir_path, name_of_data)
        name_valid = (name_of_data.endswith('.txt') or name_of_data.endswith('.csv')and name_of_data.find(' ') == -1)
        
        if name_valid and Path(save_data_path).exists():
            nanostringtextdata_tocsvdata(name_of_data)
            messages.info(request, f"Text file {save_data_path} EXISTS. It has been used to write {name_of_data.replace('txt', 'csv')}.")
            return redirect('pages:messages_page', 'download-data')

        elif name_valid:
            dataurl = f'http://nanostring-public-share.s3-website-us-west-2.amazonaws.com/GeoScriptHub/KidneyDataset/{name_of_data}'
            try:
                with urllib.request.urlopen(dataurl) as nanostringData:
                    with open(save_data_path, mode='w', newline=None) as resultsInTxt:
                        theData = nanostringData.read()
                        text_data = theData.decode(encoding="utf-8", errors="strict").replace('\t', ',').replace('\r\n', '\n').strip()
                        resultsInTxt.write(text_data)

                if Path(save_data_path).exists:
                    messages.success(request, f"Text file {save_data_path} is successfully created.")
                    nanostringtextdata_tocsvdata(name_of_data)
                    return redirect('pages:messages_page', 'download-data')
                else:
                    messages.warning(request, f"Text file {name_of_data} WAS NOT created.")
                    return redirect('pages:messages_page', 'download-data')

            except urllib.error.URLError:
                messages.warning(request, f"URLError is raised because there is no network connection.")
                return redirect('pages:messages_page', 'download-data')


    context = {
        'page_name': 'Download/Rewrite Data',
        'download_form': download_form,
        'save_dir_path': save_dir_path,
    }

    return render(request, template_name, context)



def disease2BScanVectorized_view(request):

    template_name = 'pages/disease2BScanVectorized.html'

    disease2BScanVectorized = Disease2BScanVectorized.objects.order_by('fid')

    context = {'page_name': 'Disease2BScanVectorized Data',}


    if disease2BScanVectorized:

        disease2BScanVectorized_geojson = serialize(
            'geojson',
            disease2BScanVectorized,
            srid=3857,
        )

        context = {
            'page_name': 'Disease2BScanVectorized Data',
            'disease2BScanVectorized_geojson': disease2BScanVectorized_geojson,
        }

    return render(request, template_name, context)



def normal2BScanVectorized_view(request):

    template_name = 'pages/normal2BScanVectorized.html'

    normal2BScanVectorized = Normal2BScanVectorized.objects.order_by('fid')

    context = {'page_name': 'Normal2BScanVectorized Data',}

    if normal2BScanVectorized:

        normal2BScanVectorized_geojson = serialize(
            'geojson',
            normal2BScanVectorized,
            srid=3857,
        )

        context = {
            'page_name': 'Normal2BScanVectorized Spatial Data',
            'normal2BScanVectorized_geojson': normal2BScanVectorized_geojson,
        }

    return render(request, template_name, context)



def disease2bscan_update_view(request, scan_fid):
    template_name = 'pages/disease2bscan_update.html'

    scan_to_update = get_object_or_404(Disease2BScanVectorized, fid=scan_fid)

    scan_update_form = Disease2BScanVectorizedModelForm(request.POST or None, instance=scan_to_update)
    if scan_update_form.is_valid():
        scan_update_form.save()
        messages.success(request, f'Disease2BScan Vectorized Image of fid {scan_to_update.fid} successfully updated.')
        return redirect('pages:messages_page', 'disease2b-scan')
    
    context = {
        'page_name': 'Update Disease2BScanVector',
        'scan_update_form': scan_update_form,
        'scan_to_update': scan_to_update,
    }

    return render(request, template_name, context)




def normal2bscan_update_view(request, scan_fid):
    template_name = 'pages/normal2bscan_update.html'

    scan_to_update = get_object_or_404(Normal2BScanVectorized, fid=scan_fid)

    scan_update_form = Normal2BScanVectorizedModelForm(request.POST or None, instance=scan_to_update)
    if scan_update_form.is_valid():
        scan_update_form.save()
        messages.success(request, f'Normal2BScanVectorized of id {scan_to_update.fid} successfully updated.')
        return redirect('pages:messages_page', 'normal2b-scan')
    
    context = {
        'page_name': 'Update Normal2BScanVector',
        'scan_update_form': scan_update_form,
        'scan_to_update': scan_to_update,
    }

    return render(request, template_name, context)



def disease2bscan_delete_view(request, scan_fid):
    template_name = 'pages/disease2bscan_delete.html'

    scan_to_delete = get_object_or_404(Disease2BScanVectorized, fid=scan_fid)

    if request.method == 'POST':
        scan_to_delete.delete()
        messages.success(request, f'Disease2BScanVectorized successfully deleted.')
        return redirect('pages:messages_page', 'disease2b-scan')
    
    context = {
        'page_name': 'Delete Disease2BScanVector',
        'scan_to_delete': scan_to_delete,
    }

    return render(request, template_name, context)




def normal2bscan_delete_view(request, scan_fid):
    template_name = 'pages/normal2bscan_delete.html'

    scan_to_delete = get_object_or_404(Normal2BScanVectorized, fid=scan_fid)

    if request.method == 'POST':
        scan_to_delete.delete()
        messages.success(request, f'Normal2BScanVectorized successfully deleted.')
        return redirect('pages:messages_page', 'normal2b-scan')
    
    context = {
        'page_name': 'Delete Normal2BScanVector',
        'scan_to_delete': scan_to_delete,
    }

    return render(request, template_name, context)



def analyses_tables(
    request,
    file_name, #str
    theDF, #the csv handler retrning the DF
    modelSearchForm,
    quantileSearchForm
    ):

    csv_obj = RawCSVFiles.objects.get(file_name=file_name),
    data_DF = theDF()
    search_count = len(data_DF)
    columns_list = list(data_DF.columns.values)
    data_DF_describe_table = data_DF.describe().to_html(
        justify='center', show_dimensions=True, classes=['table', 'table-bordered', 'table-striped']
    )

    model_search_form = modelSearchForm(request.GET or None)

    search_value = None
    search_record_table = None
    if model_search_form.is_valid() and 'search_value' in request.GET:
        cd = model_search_form.cleaned_data
        search_value = cd['search_value']
        new_DF = data_DF.loc[[search_value]]
        search_record_table = new_DF.to_html(
            justify='center', show_dimensions=True, classes=['table', 'table-bordered', 'table-striped']
        )
        
            
    quantiles_1_2_3 = data_DF.dropna().quantile([.25, .5, .75]).to_html(
        justify='center', show_dimensions=True, classes=['table', 'table-bordered', 'table-striped']
    )
    
    quantile_search_table = None
    quantile_search_percentage = None
    quantile_search_value = None
    quantile_search_form = quantileSearchForm(request.GET or None)
    
    if quantile_search_form.is_valid() and 'quantile_value' in request.GET:
        q_cd = quantile_search_form.cleaned_data
        quantile_search_value = float(q_cd['quantile_value'])
        quantile_search_percentage = round(quantile_search_value * 100, 2)
        quantile_search_table = data_DF.quantile([quantile_search_value]).to_html(
            justify='center', show_dimensions=True, classes=['table', 'table-bordered', 'table-striped']
        )

    return {
        'csv_obj': csv_obj,
        'search_count': search_count,
        'columns_count': len(columns_list),
        'search_form': model_search_form,
        'data_DF_describe_table': data_DF_describe_table,
        'search_value': search_value,
        'search_record_table': search_record_table,
        'quantiles_1_2_3': quantiles_1_2_3,
        'quantile_search_form': quantile_search_form,
        'quantile_search_percentage': quantile_search_percentage,
        'quantile_search_table': quantile_search_table,
    }



def draw_bar_charts(
    dataframe,
    df_title,
    x_name,
    x_label,
    y_name,
    y_label,
    tooltips:list, legend_field, fill_color='Color',
    legend_orientation="vertical",
    legend_location = "top_center"
):
    data_CDS = ColumnDataSource(dataframe)
    
    b_graph=figure(
        title=df_title,
        x_axis_label=x_label,
        y_axis_label=y_label,
        # width = 992,
        # height = 600,
        tooltips = tooltips,
        # x_range=list(x_range),
        # plot_width=1200,
        # plot_height=500,
        # toolbar_location='below',
        )
        
    
    b_graph.vbar(
        x=x_name,
        top=y_name,
        source=data_CDS,
        width=0.8,
        legend_field=legend_field,
        fill_color=fill_color,
        line_color ='#ffffff',
        )

    b_graph.toolbar.active_drag = None
    b_graph.title.align = "center"
    b_graph.title.text_color = "darkgreen"
    b_graph.title.text_font_size = "18px"
    b_graph.xaxis.major_label_text_color = 'darkgreen'
    b_graph.yaxis.major_label_text_color = 'darkgreen'
    b_graph.xgrid.grid_line_color = None
    b_graph.y_range.start=0
    b_graph.legend.orientation=legend_orientation
    b_graph.legend.location = legend_location


    b_graph_script, b_graph_div = components(b_graph)

    return {
        'b_graph_script': b_graph_script,
        'b_graph_div': b_graph_div,
    }



# Draw Nested Bars for each category
def draw_bar_nested(dataframe, n_bar_title):
    
    # dataframe
    data_DF = dataframe()

    list_max = list(data_DF.max())
    list_mean = list(data_DF.mean())
    list_min = list(data_DF.min())
    
    x= [(col,measure) for col in list(data_DF.columns) for measure in ['max', 'mean', 'min']]
    counts = sum(zip(list_max, list_mean, list_min), ())

    source = ColumnDataSource(data=dict(x=x, counts=counts))
    
    bar_nested = figure(
        x_range=FactorRange(*x),
        plot_width=(60 * len(list(data_DF.columns))),
        title=n_bar_title,
    )

    bar_nested.vbar(x='x', top='counts', width=0.5, source=source)

    bar_nested.y_range.start = 0
    bar_nested.x_range.range_padding = 0.005
    bar_nested.title.align = "left"
    bar_nested.title.text_color = "#002b80"
    bar_nested.title.text_font_size = "18px"
    bar_nested.xaxis.major_label_orientation = pi/2
    bar_nested.xaxis.group_label_orientation = pi/2
    bar_nested.xaxis.group_text_color = "#002b80"
    bar_nested.xaxis.group_text_font_size = "14px"
    bar_nested.xaxis.group_text_font_style = "bold"
    bar_nested.ygrid.grid_line_color = '#e6e6e6'
    bar_nested.xgrid.grid_line_color = None

    script_bar_nested, div_bar_nested = components(bar_nested)

    return {
        'script_bar_nested': script_bar_nested,
        'div_bar_nested': div_bar_nested,
    }



# find the outliers for each category
def draw_boxplots(dataframe, boxplot_title):

    # dataframe
    data_DF = dataframe()

    # find the quartiles and IQR for each category
    q1 = data_DF.quantile(q=0.25)
    q2 = data_DF.quantile(q=0.5)
    q3 = data_DF.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr


    def outliers(series):
        series_name = series.name
        return series[(series > upper.loc[series_name]) | (series < lower.loc[series_name])]

    applied_DF = data_DF.apply(outliers).dropna()

    # prepare outlier data for plotting, we need coordinates for every outlier.
    if not applied_DF.empty:
        applied_DF_x = list(applied_DF.index.get_level_values(0))
        applied_DF_y = list(applied_DF.values)


    dataframe_cols = list(data_DF.columns)
    box_plot = figure(
        title=boxplot_title,
        width=(60 * len(dataframe_cols)),
        height=800,
        tools="",
        background_fill_color="#ffffff",
        x_range=dataframe_cols,
        toolbar_location=None
    )
    box_plot.xaxis.major_label_orientation = pi/2
    box_plot.xaxis.major_label_text_color = "#663366"
    box_plot.xaxis.major_label_text_font_style = 'bold'
    box_plot.xaxis.major_label_text_font_size = "14px"
    box_plot.title.align = "left"
    box_plot.title.text_color = "#009999"
    box_plot.title.text_font_size = "18px"
    box_plot.ygrid.grid_line_color = '#e6e6e6'
    box_plot.ygrid.minor_grid_line_color = '#f2f2f2'
    
    # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
    qmin = data_DF.quantile(q=0.00)
    qmax = data_DF.quantile(q=1.00)
    upper = [min([x,y]) for (x,y) in zip(list(qmax.loc[:]),upper)]
    lower = [max([x,y]) for (x,y) in zip(list(qmin.loc[:]),lower)]

    
    # stems
    box_plot.segment(dataframe_cols, upper, dataframe_cols, q3, line_color="#660066")
    box_plot.segment(dataframe_cols, lower, dataframe_cols, q1, line_color="#660066")

    # boxes
    box_plot.vbar(dataframe_cols, 0.7, q2, q3, fill_color="#996600", line_color="#999999")
    box_plot.vbar(dataframe_cols, 0.7, q1, q2, fill_color="#009966", line_color="#666666")

    # whiskers (almost-0 height rects simpler than segments)
    box_plot.rect(dataframe_cols, lower, 0.2, 0.01, line_color="black")
    box_plot.rect(dataframe_cols, upper, 0.2, 0.01, line_color="black")

    # outliers
    if not applied_DF.empty:
        box_plot.circle(applied_DF_x, applied_DF_y, size=6, color="#F38630", fill_alpha=0.6)

    box_plot.xgrid.grid_line_color = None
    box_plot.ygrid.grid_line_color = "white"
    box_plot.grid.grid_line_width = 2
    box_plot.xaxis.major_label_text_font_size="12px"

    script_box_plot, div_box_plot = components(box_plot)

    return {
        'script_box_plot': script_box_plot,
        'div_box_plot': div_box_plot,
    }




def draw_star(
    dataframe, line_title, x_field, y_field,
    color, tooltips:list, legend_field,
    x_axis_label, y_axis_label
):
    # line(x={'field': 'x'}, y={'field': 'y'}, *, line_alpha=1.0, line_cap='butt', line_color='black',...)
    
    # dataframe
    try:
        data_DF = dataframe()
    except TypeError:
        data_DF = dataframe
        

    # CDS source
    source = ColumnDataSource(data_DF)

    

    # Star figure
    star_fig = figure(
        title=line_title,
        plot_height=600,
        plot_width=992,
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
        tooltips=tooltips,
    )
    star_fig.star(
        x_field,
        y_field,
        size=12,
        color=color,
        source=source,
        legend_field=legend_field,
    )

    star_fig.title.align = "center"
    star_fig.title.text_color = "#660066"
    star_fig.title.text_font_size = "18px"
    star_fig.toolbar.active_drag = None
    star_fig.legend.orientation = "vertical"
    star_fig.legend.location = "top_left"
    star_fig.xaxis.major_label_text_font_size = "14px"
    star_fig.yaxis.major_label_text_font_size = "12px"
    star_fig.xaxis.formatter.use_scientific = False
    star_fig.yaxis.formatter.use_scientific = False


    script_star_plot, div_star_plot = components(star_fig)
    

    return {
        'script_star_plot':script_star_plot,
        'div_star_plot':div_star_plot,
    }



class CategoryList(ListView):
    model = Category


def set_categories_view(request):
    template_name = 'pages/set_data_categories.html'

    category_form = CategoryModelForm(request.POST or None)
    if category_form.is_valid() and 'name' in request.POST:
        category_form.save()
        added_category = Category.objects.get(name=category_form.cleaned_data['name'])
        messages.success(request, f'{added_category.get_name_display().upper()} has been Added')
        return redirect('pages:messages_page', 'set-data-categories')

    context = {
        'page_name': 'Add Data Categories',
        'category_form': category_form,
    }

    return render(request, template_name, context)



def update_category_view(request, obj_name):
    template_name = 'pages/update_data_categories.html'
    category = get_object_or_404(Category, name=obj_name)

    category_form = CategoryModelForm(request.POST or None, instance=category)
    if category_form.is_valid() and 'name' in request.POST:
        category_form.save()
        added_category = Category.objects.get(name=category_form.cleaned_data['name'])
        messages.success(request, f'{added_category.get_name_display().upper()} has been Updated')
        return redirect('pages:messages_page', 'data-categories')

    context = {
        'page_name': 'Data Categories',
        'category_form': category_form,
    }

    return render(request, template_name, context)



def upload_csvs_view(request):
    template_name = 'pages/upload_csvs.html'
    uploadForm = UploadRawCSVFilesModelForm()

    if request.method == 'POST':
        uploadForm = UploadRawCSVFilesModelForm(request.POST or None, request.FILES)
    
        if uploadForm.is_valid() and 'file_name' in request.POST:
            uploaded_file = request.FILES['file']

            # check if its csv
            if not uploaded_file.name.endswith('.csv'):
                messages.error(request, 'Uploaded file is not a csv!')
                return redirect('pages:messages_page', 'upload-csvs')

            # check if name of csv and file matches
            if not uploaded_file.name == uploadForm.cleaned_data['file_name']:
                messages.error(request, 'Stated and Uploaded csv names do not match!')
                return redirect('pages:messages_page', 'upload-csvs')
            
            new_data, created = RawCSVFiles.objects.update_or_create(
                file_name=uploadForm.data['file_name'],
                defaults={'file':uploaded_file}
            )

            if created:
                messages.success(request, f'{uploaded_file.name} has been Uploaded')
                return redirect('pages:messages_page', 'upload-csvs')
            else:
                messages.success(request, f'Updated existing {uploaded_file.name}')
                return redirect('pages:messages_page', 'upload-csvs')

    csv_files_count = all_raw_csv_files.count()

    context = {
        'page_name': 'Upload CSV files',
        'uploadForm': uploadForm,
        'all_raw_csv_files': all_raw_csv_files.order_by('file_name'),
        'csv_files_count': csv_files_count,
    }

    return render(request, template_name, context)



def home_page_view(request):
    template_name = 'pages/homepage.html'
    
    feature_annotations_dataframe = None
    if feature_annotations_DF() is not None:
        feature_annotations_dataframe = feature_annotations_DF().head().to_html(
            justify='center', show_dimensions=True, classes=['table table-bordered table-sm']
        )

    probe_expression_dataframe = None
    if probe_expression_DF() is not None:
        probe_expression_dataframe = probe_expression_DF().head().to_html(
            justify='center', show_dimensions=True, classes=['table', 'table-bordered', 'table-sm']
        )

    target_expression_dataframe = None
    if target_expression_DF() is not None:
        target_expression_dataframe = target_expression_DF().head().to_html(
            justify='center', show_dimensions=True, classes=['table', 'table-bordered', 'table-sm']
        )

    normalized_expression_dataframe = None
    if normalized_expression_DF() is not None:
        normalized_expression_dataframe = normalized_expression_DF().head().to_html(
            justify='center', show_dimensions=True, classes=['table', 'table-bordered', 'table-sm']
        )
    

    single_sample_gsea_results_dataframe = None
    if ssGSEA_expression_DF() is not None:
        single_sample_gsea_results_dataframe = ssGSEA_expression_DF().rename(columns={"Unnamed: 0.1": "Name"}).head().to_html(
            justify='center', show_dimensions=True, classes=['table', 'table-bordered', 'table-sm']
        )

    average_gene_dataframe = None
    if average_gene_expression_DF() is not None:
        average_gene_dataframe = average_gene_expression_DF().head().to_html(
            justify='center', show_dimensions=True, classes=['table', 'table-bordered', 'table-sm']
        )
    

    context = {
        'page_name': 'Home',
        'cell_types': all_cell_types[0:3],
        'sample_annotations': all_sample_annotations_types[0:3],
        'Kidney_Feature_Annotations': all_raw_csv_files.filter(file_name='Kidney_Feature_Annotations.csv'),
        'feature_annotations_dataframe': feature_annotations_dataframe,
        'kidney_raw_bioProbeCountMatrix': all_raw_csv_files.filter(file_name='Kidney_Raw_BioProbeCountMatrix.csv'),
        'probe_expression_dataframe': probe_expression_dataframe,
        'kidney_raw_target_count_matrix': all_raw_csv_files.filter(file_name='Kidney_Raw_TargetCountMatrix.csv'),
        'target_expression_dataframe': target_expression_dataframe,
        'kidney_q3_norm_target_count_matrix': all_raw_csv_files.filter(file_name='Kidney_Q3Norm_TargetCountMatrix.csv'),
        'normalized_expression_dataframe': normalized_expression_dataframe,
        'Kidneyss_GSEA': all_raw_csv_files.filter(file_name='Kidney_ssGSEA.csv'),
        'single_sample_gsea_results_dataframe': single_sample_gsea_results_dataframe,
        'average_gene_expression': all_raw_csv_files.filter(file_name='Young_kidney_cell_profile_matrix.csv'),
        'average_gene_dataframe': average_gene_dataframe,
    }

    return render(request, template_name, context)



def messages_view(request, prev_name=None):
    template_name = 'pages/messages.html'

    context = {
        'page_name': 'Messages',
    }

    return render(request, template_name, context)




def foss_licenses_page_view(request):
    template_name = 'pages/foss_licenses.html'

    context = {
        'page_name': 'FOSS Licenses',
        'bokeh_license': bokeh_license(),
        'bootstrap_license': bootstrap_license(),
        'django_license': django_license(),
        'openlayers_license': openlayers_license(),
        'python_license': python_license(),
        'qgis_license': qgis_license(),
    }

    return render(request, template_name, context)



class SampleAnnotationList(ListView):
    model = Kidney_Sample_Annotations
    paginate_by = 60



class CellTypeList(ListView):
    model = Cell_Types_for_Spatial_Decon



def kidney_sample_annotations_uploader_view(request):
    template_name = 'pages/sampleannotation_upload.html'
    sample_annotations_form = UploadSampleAnnotationsForm()

    if request.method == 'POST':
        sample_annotations_form = UploadSampleAnnotationsForm(request.POST, request.FILES)
        if sample_annotations_form.is_valid():
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



def sample_annotations_analysis_view(request):
    template_name = 'pages/sample_annotation_analysis.html'
    sample_annotations = Kidney_Sample_Annotations.objects.order_by('id')
    search_count = sample_annotations.count()
    

    # sample_annotations_DF = DataFrame(sample_annotations_data, columns=['disease_status', 'segment_display_name'])
    sample_annotations_DF = DataFrame(sample_annotations.values())
    
    
    data_DF_describe_table = sample_annotations_DF.describe().to_html(
        justify='center', show_dimensions=True, classes=['table', 'table-bordered', 'table-striped']
    )
    

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

        sample_annotations_DF = DataFrame(sample_annotations.values())

        if sample_annotations.count() == 0:
            messages.error(request, f'No Sample Annotations matches: "{search_value}".')
            return redirect('pages:messages_page', 'sample-annotations-analysis')
        else:
            search_count = sample_annotations.count()


    sample_annotations_vector_geoson = serialize(
        'geojson',
        sample_annotations,
        geometry_field='geom',
        srid=3857,
        fields=('disease_status','segment_display_name')
        )
        

    disease_status_group = sample_annotations_DF.groupby(['disease_status']).count()

    # Create value column to be used for piechart angles
    disease_status_group['value'] = (
        disease_status_group['segment_display_name']/len(sample_annotations_DF) * 2*pi
        )
    disease_status_group['proportion'] = (
        disease_status_group['segment_display_name']
        )
    disease_status_group['color'] = ['#ff3300', '#009933'][:len(disease_status_group)]
    
    disease_status_groups_CDS = ColumnDataSource(disease_status_group)


    disease_status_group_describe_table = sample_annotations_DF[
        [
            'disease_status', 'loq', 'normalization_factor', 'raw_reads', 'trimmed_reads',
            'stitched_reads', 'aligned_reads', 'duplicated_reads', 'sequencing_saturation',
            'umiq_30', 'rtsq_30'
        ]
    ].groupby(['disease_status']).describe().to_html(
        justify='center', show_dimensions=True, classes=['table', 'table-bordered', 'table-striped']
    )
    

    sample_annotations_fig=figure(
        title="Sample Annotations categorized by Disease Status",
        # plot_height=600,
        plot_width=800,
        tooltips=[
            ('Disease Status', '@disease_status'),
            ('Proportion', f'@proportion out of {len(sample_annotations_DF)}'),
        ],
    )

    sample_annotations_fig.wedge(
        x=0,
        y=1,
        radius=0.5,
        start_angle=cumsum('value', include_zero=True),
        end_angle=cumsum('value'),
        line_color="#ffffff",
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
    
    script_pie_chart, div_pie_chart = components(sample_annotations_fig)

    quantile_search_table = None
    quantile_search_percentage = None
    quantile_search_value = None
    quantile_search_form = QuantileSearchForm(request.GET or None)

    numerical_cols = [
        'roi_label',
        'aoi_surface_area',
        'aoi_nuclei_count',
        'loq', 'normalization_factor', 'raw_reads', 'trimmed_reads',
        'stitched_reads', 'aligned_reads', 'duplicated_reads', 'sequencing_saturation',
        'umiq_30', 'rtsq_30'
    ]
    
    if quantile_search_form.is_valid() and 'quantile_value' in request.GET:
        q_cd = quantile_search_form.cleaned_data
        quantile_search_value = float(q_cd['quantile_value'])
        quantile_search_percentage = round(quantile_search_value * 100, 2)
        quantile_search_table = sample_annotations_DF[numerical_cols].quantile([quantile_search_value]).to_html(
            justify='center', show_dimensions=True, classes=['table', 'table-bordered', 'table-striped']
        )

    coords_DF = DataFrame(
        sample_annotations_DF,
        columns=[
            'roi_coordinate_x',
            'roi_coordinate_y',
            'disease_status',
            'Color',
            'aoi_surface_area',
            'aoi_nuclei_count',
            'segment_display_name',
        ]
    )
    
    coords_DF.loc[coords_DF['disease_status'] == 'normal', 'Color'] = 'green'
    coords_DF.loc[coords_DF['disease_status'] == 'DKD', 'Color'] = 'red'
    
    coords_CDS = ColumnDataSource(coords_DF)

    TOOLS = TOOLS="hover,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,reset,tap,save,box_select,poly_select,"

    scatter = figure(
        title='Scatter Plot for Sample Annotations',
        plot_width=800,
        x_axis_label='X Coordinates',
        y_axis_label='Y Coordinates',
        tools=TOOLS,
    )
    scatter.scatter(
        'roi_coordinate_x',
        'roi_coordinate_y',
        size=8,
        marker="circle",
        fill_color='Color',
        line_color=None,
        source=coords_CDS
    )
    scatter.title.align = "center"
    scatter.title.text_color = "#003300"
    scatter.title.text_font_size = "18px"
    scatter.toolbar.active_drag = None
    

    script_scatter, div_scatter = components(scatter)
    
    

    star_tooltips=[
        (('Status'), ('@disease_status')),
        (('Segment Display Name'), ('@segment_display_name')),
        (('Nuclei Count'), ('@aoi_nuclei_count')),
        (('Surface Area'), ('@aoi_surface_area')),
    ]

    star_graph = draw_star(
        coords_DF,
        'Relationship between AOI Surface Area with AOI Nuclei Count',
        'aoi_nuclei_count',
        'aoi_surface_area',
        'Color',
        star_tooltips,
        'disease_status',
        'Nuclei Count',
        'Surface Area'
    )

    


    context = {
        'page_name': 'Sample Annotations Analysis',
        'sample_annotations': sample_annotations,
        'sample_annotations_search_form': sample_annotations_search_form,
        'search_count': search_count,
        'sample_annotations_vector_geoson': sample_annotations_vector_geoson,
        'script_pie_chart': script_pie_chart,
        'div_pie_chart': div_pie_chart,
        'data_DF_describe_table': data_DF_describe_table,
        'disease_status_group_describe_table': disease_status_group_describe_table,
        # 'quantiles_1_2_3': quantiles_1_2_3,
        'quantile_search_percentage': quantile_search_percentage,
        'quantile_search_table': quantile_search_table,
        'quantile_search_value': quantile_search_value,
        'quantile_search_form': quantile_search_form,
        'script_scatter': script_scatter,
        'div_scatter': div_scatter,
        'script_star_plot': star_graph['script_star_plot'],
        'div_star_plot': star_graph['div_star_plot'],
    }

    return render(request, template_name, context)



def cell_types_for_spatial_decon_uploader_view(request):
    template_name = 'pages/celltype_upload.html'
    cell_types_form = UploadCellTypesForm()

    if request.method == 'POST':
        cell_types_form = UploadCellTypesForm(request.POST, request.FILES)
        if cell_types_form.is_valid():
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
        

    data_DF_describe_table = cells_type_DF.describe().to_html(classes=['table', 'table-bordered', 'table-striped'])
    
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
        'data_DF_describe_table': data_DF_describe_table,
        'script1': script1,
        'div1': div1,
        'script2': script2,
        'div2': div2,
    }

    return render(request, template_name, context)



def feature_annotation_analysis_view(request):
    
    template_name = 'pages/kidney_feature_annotations_analysis.html'
    csv_obj = RawCSVFiles.objects.get(file_name='Kidney_Feature_Annotations.csv')
    data_DF = feature_annotations_DF()
    

    search_count = len(data_DF)
    columns_list = list(data_DF.columns.values)

    df_head = data_DF.head().to_html(
            justify='center', show_dimensions=True, classes=['table table-bordered table-striped']
        )
    

    negative_groups_count_DF = data_DF.groupby(['Negative']).count()
    negative_groups_count_DF['Value'] = (
        negative_groups_count_DF['ProbeID']/negative_groups_count_DF['ProbeID'].sum() * 2*pi
        )
        
    negative_groups_count_DF['Color'] = ['#cce5ff', '#cc00cc']
    data_DF_describe_table = negative_groups_count_DF.to_html(
        justify='center', show_dimensions=True, classes=['table table-bordered table-striped']
    )
    data_CDS = ColumnDataSource(negative_groups_count_DF)

    pie_chart_tooltips= [
        ('Negative', '@Negative'),
        ('Proportion', f'@ProbeID out of {negative_groups_count_DF["ProbeID"].sum()}'),
    ]


    pie_chart = figure(
        title="Pie Chart showing Proportions of Negative for Feature Annotations",
        width = 992,
        height = 600,
        background_fill_color = '#e6f2ff',
        outline_line_color = '#0066cc',
        tooltips=pie_chart_tooltips,
    )

    pie_chart.wedge(
        x=0,
        y=1,
        radius=0.5,
        start_angle=cumsum('Value', include_zero=True),
        end_angle=cumsum('Value'),
        line_color="#ffffff",
        fill_color='Color',
        source=data_CDS,
        legend_field='Negative',
        )

    pie_chart.axis.visible=False
    pie_chart.axis.axis_line_color=None
    pie_chart.toolbar.active_drag = None
    pie_chart.title.align = "center"
    pie_chart.title.text_color = "#003e80"
    pie_chart.title.text_font_size = "18px"
    pie_chart.legend.orientation = "vertical"
    pie_chart.legend.location = "right"
    
    pie_script, pie_div = components(pie_chart)

    search_value = None
    search_record_table = None
    search_form = SearchFeatureAnnotationsForm(request.GET or None)
    if search_form.is_valid() and 'search_value' in request.GET:
        cd = search_form.cleaned_data
        search_value = cd['search_value']
        try:
            new_DF = data_DF.loc[[search_value]]
            search_record_table = new_DF.to_html(
                justify='center', show_dimensions=True, classes=['table', 'table-bordered', 'table-striped']
            )
        except KeyError:
            messages.error(request, f'No Feature Annotation (RTS_ID) matches: <h1 class="display-4">{search_value}</h1>')
            return redirect('pages:messages_page', 'feature-annotations-analysis')


    tooltips= [
        ('Negative', '@Negative'),
        ('Proportion', f'@ProbeID out of {negative_groups_count_DF["ProbeID"].sum()}'),
    ]
    bar_chart = draw_bar_charts(
        negative_groups_count_DF,
        "Bar Graph Showing Proportions of Negative for Feature Annotations",
        'Negative',
        'Negative',
        'ProbeID',
        '',
        tooltips,
        'Negative',
        'Color',
        'horizontal',
        'center_right'
    )
    

    context = {
        'page_name': 'Feature Annotation Analysis',
        'csv_obj': csv_obj,
        'data_DF': data_DF,
        'search_count': search_count,
        'columns_count': len(columns_list),
        'data_DF_describe_table': data_DF_describe_table,
        'df_head': df_head,
        'pie_script': pie_script,
        'pie_div': pie_div,
        'search_form': search_form,
        'search_value': search_value,
        'search_record_table': search_record_table,
        'b_graph_script': bar_chart['b_graph_script'],
        'b_graph_div': bar_chart['b_graph_div'],
    }

    return render(request, template_name, context)
    


def kidney_raw_bioProbeCountMatrix_analysis_view(request):
    
    
    try:
        analysis_context = analyses_tables(
            request,
            'Kidney_Raw_BioProbeCountMatrix.csv',
            probe_expression_DF,
            SearchProbeExpressionForm,
            QuantileSearchForm,
        )

        
        template_name = 'pages/probe_expression_analysis.html'
        box_plot = draw_boxplots(probe_expression_DF, 'Boxplot for Probe Expressions')
        nested_bar = draw_bar_nested(probe_expression_DF, 'Nested Bar Plot for Probe Expressions')

        context = {
            'page_name': 'Probe Expressions',
            'csv_obj': analysis_context['csv_obj'],
            'search_count': analysis_context['search_count'],
            'columns_count': analysis_context['columns_count'],
            'search_form': analysis_context['search_form'],
            'data_DF_describe_table': analysis_context['data_DF_describe_table'],
            'search_value': analysis_context['search_value'],
            'search_record_table': analysis_context['search_record_table'],
            'quantiles_1_2_3': analysis_context['quantiles_1_2_3'],
            'quantile_search_form': analysis_context['quantile_search_form'],
            'quantile_search_percentage': analysis_context['quantile_search_percentage'],
            'quantile_search_table': analysis_context['quantile_search_table'],
            'script_box_plot': box_plot['script_box_plot'],
            'div_box_plot': box_plot['div_box_plot'],
            'script_bar_nested': nested_bar['script_bar_nested'],
            'div_bar_nested': nested_bar['div_bar_nested'],
        }

        return render(request, template_name, context)
        
    except KeyError:
        search_value = SearchProbeExpressionForm(request.GET).data['search_value']
        messages.error(request, f'No Probe Expressions (ProbeName) matches: <h1 class="display-4">{search_value}</h1>')
        return redirect('pages:messages_page', 'probe-expression-analysis')



def KidneyRawTargetCountMatrix_analysis_view(request):
    
    try:
        data_DF = target_expression_DF
        analysis_context = analyses_tables(
            request,
            'KidneyRawTargetCountMatrix',
            data_DF,
            SearchTargetExpressionForm,
            QuantileSearchForm,
        )

        
        template_name = 'pages/target_expression_analysis.html'
        box_plot = draw_boxplots(data_DF, 'Boxplot for Target Expressions')
        nested_bar = draw_bar_nested(data_DF, 'Nested Bar Plot for Target Expressions')



        context = {
            'page_name': 'Target Expressions',
            'csv_obj': analysis_context['csv_obj'],
            'search_count': analysis_context['search_count'],
            'columns_count': analysis_context['columns_count'],
            'search_form': analysis_context['search_form'],
            'data_DF_describe_table': analysis_context['data_DF_describe_table'],
            'search_value': analysis_context['search_value'],
            'search_record_table': analysis_context['search_record_table'],
            'quantiles_1_2_3': analysis_context['quantiles_1_2_3'],
            'quantile_search_form': analysis_context['quantile_search_form'],
            'quantile_search_percentage': analysis_context['quantile_search_percentage'],
            'quantile_search_table': analysis_context['quantile_search_table'],
            'script_box_plot': box_plot['script_box_plot'],
            'div_box_plot': box_plot['div_box_plot'],
            'script_bar_nested': nested_bar['script_bar_nested'],
            'div_bar_nested': nested_bar['div_bar_nested'],
        }

        return render(request, template_name, context)
        
    except KeyError:
        search_value = SearchProbeExpressionForm(request.GET).data['search_value']
        messages.error(request, f'No Target Expressions (TargetName) matches: <h1 class="display-4">{search_value}</h1>')
        return redirect('pages:messages_page', 'target-expression-analysis')



def KidneyQ3NormTargetCountMatrix_analysis_view(request):
    
    try:
        data_DF = normalized_expression_DF
        analysis_context = analyses_tables(
            request,
            'KidneyQ3NormTargetCountMatrix',
            data_DF,
            SearchNormalizedExpressionForm,
            QuantileSearchForm,
        )

        
        template_name = 'pages/normalized_expression_analysis.html'
        box_plot = draw_boxplots(data_DF, 'Boxplot for Normalized Expressions')
        nested_bar = draw_bar_nested(data_DF, 'Nested Bar Plot for Normalized Expressions')



        context = {
            'page_name': 'Normalized Expressions',
            'csv_obj': analysis_context['csv_obj'],
            'search_count': analysis_context['search_count'],
            'columns_count': analysis_context['columns_count'],
            'search_form': analysis_context['search_form'],
            'data_DF_describe_table': analysis_context['data_DF_describe_table'],
            'search_value': analysis_context['search_value'],
            'search_record_table': analysis_context['search_record_table'],
            'quantiles_1_2_3': analysis_context['quantiles_1_2_3'],
            'quantile_search_form': analysis_context['quantile_search_form'],
            'quantile_search_percentage': analysis_context['quantile_search_percentage'],
            'quantile_search_table': analysis_context['quantile_search_table'],
            'script_box_plot': box_plot['script_box_plot'],
            'div_box_plot': box_plot['div_box_plot'],
            'script_bar_nested': nested_bar['script_bar_nested'],
            'div_bar_nested': nested_bar['div_bar_nested'],
        }

        return render(request, template_name, context)
        
    except KeyError:
        search_value = SearchProbeExpressionForm(request.GET).data['search_value']
        messages.error(request, f'No Normalized Expressions (TargetName) matches: <h1 class="display-4">{search_value}</h1>')
        return redirect('pages:messages_page', 'normalized-expression-analysis')



def kidneyssGSEA_analysis_view(request):
    
    try:
        data_DF = ssGSEA_expression_DF
        analysis_context = analyses_tables(
            request,
            'KidneyssGSEA',
            data_DF,
            SearchKidneyssGSEAForm,
            QuantileSearchForm,
        )

        
        template_name = 'pages/KidneyssGSEA_analysis.html'
        box_plot = draw_boxplots(data_DF, 'Boxplot for KidneyssGSEA')
        nested_bar = draw_bar_nested(data_DF, 'Nested Bar Plot for KidneyssGSEA')



        context = {
            'page_name': 'KidneyssGSEA',
            'csv_obj': analysis_context['csv_obj'],
            'search_count': analysis_context['search_count'],
            'columns_count': analysis_context['columns_count'],
            'search_form': analysis_context['search_form'],
            'data_DF_describe_table': analysis_context['data_DF_describe_table'],
            'search_value': analysis_context['search_value'],
            'search_record_table': analysis_context['search_record_table'],
            'quantiles_1_2_3': analysis_context['quantiles_1_2_3'],
            'quantile_search_form': analysis_context['quantile_search_form'],
            'quantile_search_percentage': analysis_context['quantile_search_percentage'],
            'quantile_search_table': analysis_context['quantile_search_table'],
            'script_box_plot': box_plot['script_box_plot'],
            'div_box_plot': box_plot['div_box_plot'],
            'script_bar_nested': nested_bar['script_bar_nested'],
            'div_bar_nested': nested_bar['div_bar_nested'],
        }

        return render(request, template_name, context)
        
    except KeyError:
        search_value = SearchProbeExpressionForm(request.GET).data['search_value']
        messages.error(request, f'No KidneyssGSEA matches: <h1 class="display-4">{search_value}</h1>')
        return redirect('pages:messages_page', 'kidneyssGSEA-analysis')



def average_gene_expression_analysis_view(request):
    
    try:
        data_DF = average_gene_expression_DF
        analysis_context = analyses_tables(
            request,
            'AverageGeneExpression',
            data_DF,
            SearchAverageGeneExpressionForm,
            QuantileSearchForm,
        )

        
        template_name = 'pages/average_gene_expression_analysis.html'
        box_plot = draw_boxplots(data_DF, 'Boxplot for Average Gene Expression')
        nested_bar = draw_bar_nested(data_DF, 'Nested Bar Plot for Gene Expressions')



        context = {
            'page_name': 'Average Gene Expression',
            'csv_obj': analysis_context['csv_obj'],
            'search_count': analysis_context['search_count'],
            'columns_count': analysis_context['columns_count'],
            'search_form': analysis_context['search_form'],
            'data_DF_describe_table': analysis_context['data_DF_describe_table'],
            'search_value': analysis_context['search_value'],
            'search_record_table': analysis_context['search_record_table'],
            'quantiles_1_2_3': analysis_context['quantiles_1_2_3'],
            'quantile_search_form': analysis_context['quantile_search_form'],
            'quantile_search_percentage': analysis_context['quantile_search_percentage'],
            'quantile_search_table': analysis_context['quantile_search_table'],
            'script_box_plot': box_plot['script_box_plot'],
            'div_box_plot': box_plot['div_box_plot'],
            'script_bar_nested': nested_bar['script_bar_nested'],
            'div_bar_nested': nested_bar['div_bar_nested'],
        }

        return render(request, template_name, context)
        
    except KeyError:
        search_value = SearchProbeExpressionForm(request.GET).data['search_value']
        messages.error(request, f'No KidneyssGSEA matches: <h1 class="display-4">{search_value}</h1>')
        return redirect('pages:messages_page', 'average-gene-expression-analysis')
