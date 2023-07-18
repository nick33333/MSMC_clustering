from plotly.subplots import make_subplots
import plotly.graph_objects as go
from tslearn.metrics import dtw, dtw_path
import matplotlib.pyplot as plt
import numpy as np
import colorsys
import copy


from MSMC_clustering import *

'''
Functions in this module are used in plotting and updating the curve cluster heatmap

User should be able to add in whatever kind (normalized/unnormalized/transformed/
untransformed data) to cluster plots.

LAYOUT IDEA:
- cluster plots can be on right
- On the left can be a column with dropdown/input settings prompting the user
  for their desired Msmc_clustering settings like data processing and 
  input data.
  - Submit button can be below this column to update:
    - Plot
    - Dicts
    - Distance matrices
'''

def compute_label2series_names_and_name2trace_index(Msmc_clustering, km=None):
    '''
    Uses a km from Msmc_clustering or hand fed km to produce predictions.
    For each prediction, 
    Outputs:
    - name2trace_index
    - label2series_names: PREDICTIONS CAN BE DONE HERE! HUGE DATASTRUCT
    '''
    K = Msmc_clustering.manual_cluster_count
    name2trace_index = dict()
    label2series_names = {k: [] for k in range(K)}
    if km is not None:
        print("using given km")
        km = km
    else:
        print("using trained km")
        assert Msmc_clustering.km is not None
        km = Msmc_clustering.km
    # Predictions iterate over mySeries/namesofMySeries
    for idx, training_data in enumerate(Msmc_clustering.to_training_data()):
#         print('idx', idx)
#         print(training_data.shape)
        name = Msmc_clustering.namesofMySeries[idx]
        label = int(km.predict(np.array([training_data])))
#         print(label, type(label))
        name2trace_index[name] = idx
        label2series_names[label].append(name)
        
    return label2series_names, name2trace_index


def compute_intra_cluster_dtw_dist_matrix(Msmc_clustering,
                                          label2series_names):
    '''
    Given that we have K cluster, this function computes K distance matrices
    for samples in each of the K clusters.Msmc_clustering holds time series
    data for each of these clusters.
    
    inputs:
    - Msmc_clustering: Msmc_clustering instance (can be clustered or unclustered)
    - label2series_names: dict mapping cluster labels to a list of series
                          names. Can be computed using the compute_label2series_names
                          function if Msmc_clustering is clustered. Else it would 
                          be best to make a label2series_names-like dict after
                          calls to km.predict() (especially in app).

    outputs:
    - label2dist_matrix: Maps each distance matrix to its corresponding cluster label
    - series_series_name2label: Maps each series name to its corresponding cluster label
    '''
    # Init dicts
    label2dist_matrix = dict()
    series_name2label = dict()
    # Relevant collections
    K = Msmc_clustering.manual_cluster_count
    name2series = Msmc_clustering.name2series # dict mapping series name to series data
    for k in range(K): # For each of the K clusters in question
        namesofMySeries_k = label2series_names[k] # Method gets a list of names of samples in cluster k
        dtw_dist_matrix = []
        for i in namesofMySeries_k:
            series_name2label[i] = k
            row = []
            for j in namesofMySeries_k:
                x = name2series[i]
                y = name2series[j]
                dtw_score = dtw(x,y)
                row.append(dtw_score) # Add a column holding dtw dist between time series x and y
            dtw_dist_matrix.append(row) 
        label2dist_matrix[k] = np.array(dtw_dist_matrix)
    return label2dist_matrix, series_name2label

'''
- Select a species
- Identify its cluster
- Find DTW dist matrix within cluster
- Find N-closest species to selected species within cluster
- Update the colors of the traces corresponding to N-closest species
'''

def find_k_neighbors(series_name,
                     label2dist_matrix,
                     label2series_names,
                     series_name2label,
                     k_nearest):
    '''
    Returns a list of k nearest neighbors to a given series (in the same
    cluster) using 
    
    I'm guessing that when series_name and k_nearest change, a callback
    should be issued. series_name may change with the user's cursor/hovering
    and k_nearest might change based on a slider.
    '''
    if series_name is None: # easy default workaround
        return []
    assert series_name in series_name2label
    k = series_name2label[series_name]
    dist_matrix = label2dist_matrix[k]
    name_list = label2series_names[k]
    series_name_idx = name_list.index(series_name) # Find index of row in dist_matrix corresponding to series name
    row = dist_matrix[series_name_idx,:] # Find row containing distances of neighbors to series_name
    return sorted(list(zip(name_list, row)),key=lambda x:x[1])[:k_nearest]

'''
Everything u need to alter the colors and viewable stats of k nearest neighbors
of a time series of your choosing.
'''

def update_time_series_heatmap(series_name,
                               k_nearest,
                               immutable_data_copy,
                               label2series_names,
                               label2dist_matrix,
                               series_name2label,
                               fig,
                               name2trace_index):
    '''
    Uses dtw distance to make a heatmap styled color scheme for a selected
    sample's cluster.
    '''
    # Function calls that only need to be called once!
    mutable_data_copy = copy.deepcopy(immutable_data_copy) # Copies the data of fig right after init'ing it
    default_hovertemplate_data = mutable_data_copy[name2trace_index[series_name]]["hovertemplate"]

    k_neighbors_dists_of_name = find_k_neighbors(series_name=series_name,
                                                label2dist_matrix=label2dist_matrix,
                                                label2series_names=label2series_names,
                                                series_name2label=series_name2label,
                                                k_nearest=k_nearest)
    max_dist = max(k_neighbors_dists_of_name, key=lambda x:x[1])[1]
    for name, dist in k_neighbors_dists_of_name:
        new_hovertemplate = default_hovertemplate_data + f'<br><b>Distance to {series_name}</b>:' + f'{dist}<br>'
        (h, s, v) = ((dist/max_dist)*(80/360), 1, 1) # dist is multiplied by 80/360 to  make hsv range from red to greenish
        (r, g, b) = [255*i for i in colorsys.hsv_to_rgb(h, s, v)]
        fig.update_traces(
                          marker=dict(
                                      color=f"rgba({r}, {g}, {b}, 1)",
                                     ), 
                          hovertemplate = new_hovertemplate,
                          selector = dict(
                                          name=name
                                         ),
                         )
    return fig, k_neighbors_dists_of_name

def reset_time_series_heatmap(k_neighbors_dists_of_name,
                              immutable_data_copy,
                              name2trace_index,
                              fig):
    for name, _ in k_neighbors_dists_of_name:
        fig.update_traces(hovertemplate=immutable_data_copy[name2trace_index[name]]['hovertemplate'],
                          marker=immutable_data_copy[name2trace_index[name]]['marker'],
                          selector = ({'name':name}))
        