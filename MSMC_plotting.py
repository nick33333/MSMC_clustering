import plotly.graph_objects as go
import plotly
from MSMC_clustering import Msmc_clustering
import pandas as pd
import numpy as np
import os

def given_col_find_row(k, cols):
    '''
    k is the number of clusters. cols is the desired number of columns in
    subplot.
    '''
    if k%cols==0:
        rows = k//cols
    else:
        if k//cols == 0:
            rows = 1
        else:
            rows = k//cols + 1
    return rows


        
def given_label_find_row_col(rows, cols, label):
    '''
    Make sure label is an int. Depending on the int, a row and col is
    given
    '''

    col = (label-1)%cols + 1
    row = (label-1)//cols + 1
    
    return row, col


def add_curve_to_subplot(fig: "plotly.graph_objs._figure.Figure",
                         name,
                         cols,
                         Msmc_clustering: Msmc_clustering,
                         km=None,
                         marker_color='rgba(0, 180, 255, .8)',
                         **goScatter_kwargs):
    '''
    fig: Plotly subplot
    name: Name of curve to plot
    cols: Desired number of columns in subplot
    Msmc_clustering: Obj should hold the data and curve which you want to plot
    km: Clustering model
    '''
    series = Msmc_clustering.name2series[name]
    if isinstance(km, type(None)): # If True, Msmc_clustering must have its own km along wit hdata
        km = Msmc_clustering.km
    label = km.predict(np.array([series.to_numpy()]))
    time_field = Msmc_clustering.time_field
    value_field = Msmc_clustering.value_field
    rows = given_col_find_row(k=Msmc_clustering.manual_cluster_count, cols=cols)
    row, col =  given_label_find_row_col(rows, cols, label[0] + 1)
    fig.update_xaxes(title_text=time_field, row=row, col=col)
    fig.update_yaxes(title_text=value_field, row=row, col=col)
    
    # For line hover highlighting see https://stackoverflow.com/questions/63885102/change-color-of-an-entire-trace-on-hover-click-in-plotly
    
    subfig = go.Scatter(x=series[time_field],
                        y=series[value_field],
                        marker=dict(size=12,),
                        marker_color=marker_color,
                        name = name,
                        hovertemplate = f'<i>{name}<i>' +
                                        f'<br><b>{time_field}</b>:' + '%{x}</br>' +
                                        f'<br><b>{value_field}</b>:' + ' %{y}<br>' +
                                        '<extra></extra>', # <extra></extra> removes trace name from hover
                        **goScatter_kwargs)
    fig.add_trace(subfig, row=row, col=col)
    return