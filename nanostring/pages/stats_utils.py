from math import pi
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import (
    ColumnDataSource,
    FactorRange,
    )
from bokeh.palettes import Spectral10
from pandas import DataFrame

from sklearn.cluster import KMeans

from data.models import RawCSVFiles



def k_means_clustering(
    dataframe, x_axis, y_axis
):

    try:
        data_DF = dataframe()[[x_axis,y_axis]]
    except TypeError:
        data_DF = dataframe[[x_axis,y_axis]]

    # Number of clusters to use, identify between a range of from 1 to 10
    # WCSS (Within Cluster Sum of Squares)

    WCSS = []
    k_opts = list(range(1,10))

    for k in k_opts:
        kmod = KMeans(n_clusters=k)
        kmod.fit(data_DF)
        WCSS.append(kmod.inertia_)

    elbow_data = {'k_opts':k_opts, 'WCSS':WCSS}
    elbowDF = DataFrame(data=elbow_data)
    elbowDF['color'] = Spectral10[:len(elbowDF)]

    elbowCDS = ColumnDataSource(elbowDF)

    k_cluster_elbow = figure(
        title=f"Possible Number of Clusters to use in plotting {str(x_axis).replace('_', ' ').upper()} against {str(y_axis).replace('_', ' ').upper()}",
        width = 800,
        x_axis_label='K Options',
        y_axis_label='Within Cluster Sum of Squares',
        tooltips=[
            ('K Value', '@k_opts'),
        ],
    )
    k_cluster_elbow.diamond(
        source=elbowCDS,
        x='k_opts',
        y='WCSS',
        size=20,
        fill_color='color',
        legend_field='k_opts',
    )
    k_cluster_elbow.line(
        source=elbowCDS,
        x='k_opts',
        y='WCSS',
        line_color='#29a3a3',
    )
    k_cluster_elbow.toolbar.active_drag = None
    k_cluster_elbow.title.text_font_size = "15px"
    k_cluster_elbow.title.align = "center"

    k_cluster_elbow.xaxis.major_label_text_color = '#145252'
    k_cluster_elbow.xaxis.major_label_text_font_style = 'bold'
    k_cluster_elbow.xaxis.axis_label_text_font_style = 'bold'

    k_cluster_elbow.yaxis.major_label_text_color = '#145252'
    k_cluster_elbow.yaxis.major_label_text_font_style = 'bold'
    k_cluster_elbow.yaxis.axis_label_text_font_style = 'bold'
    

    elbow_script, elbow_div = components(k_cluster_elbow)

    return {
        'elbow_script': elbow_script,
        'elbow_div': elbow_div,
    }

    # return elbowDF.to_html()


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
        # plot_height=600,
        plot_width=800,
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
