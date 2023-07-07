sys.path.insert(1, 'MSMC_clustering/')
from MSMC_clustering import Msmc_clustering
from MSMC_plotting import *
import pandas as pd
import numpy as np
import pickle
import json
import os
import sys



# mu_dict = {'bird':1.4e-9,
#           'mammal':2.2e-9}
# time_series_path = '/scratch/nick/MSMC-Curve-Analysis/data/msmc_curve_data_birds'
# test_case_path = '/scratch/nick/MSMC-Curve-Analysis/test_case_data/'
# generation_lengths_path = '/scratch/nick/MSMC-Curve-Analysis/generation_lengths/'

# m_obj = Msmc_clustering(directory=time_series_path,
#                         mu=1.4e-9,
#                         generation_time_path=generation_lengths_path,
#                         real_time=False,
#                         normalize_lambda=True,
#                         log_scale_time=False,
#                         plot_on_log_scale=False,
#                         uniform_ts_curve_domains=False,
#                         to_omit=[],
#                         exclude_subdirs=['mammals_part_1'],
#                         manual_cluster_count=7,
#                         algo='kmeans',
#                         suffix='.txt',
#                         omit_front_prior=0,
#                         omit_back_prior=0,
#                         time_window=False,
#                         index_field='time_index',
#                         time_field='left_time_boundary',
#                         value_field='lambda',
#                         ignore_fields= ['right_time_boundary'],
#                         sep='\t')


# size_estimate = len(pickle.dumps(m_obj))

# print(size_estimate)

non_user_settings =  {'algo': 'kmeans', 'interpolation_kind': 'linear', 'interpolation_pts': '100', 'manual_cluster_count': '7', 'mu': '1.4E-9', 'omit_back_prior': '5', 'omit_front_prior': '5', 'time_field': 'left_time_boundary', 'time_window': False, 'use_interpolation': 'True', 'use_real_time_and_c_rate_transform': 'True', 'use_time_log10_scaling': 'True', 'use_value_normalization': 'True', 'value_field': 'lambda', 'directory': 'data/msmc_curve_data_birds/', 'generation_time_path': 'data/generation_lengths/', 'exclude_subdirs': [], 'use_plotting_on_log10_scale': False, 'sep': '\t'}
user_settings =  {'algo': 'kmeans', 'interpolation_kind': 'linear', 'interpolation_pts': '100', 'manual_cluster_count': '7', 'mu': '1.4E-9', 'omit_back_prior': '5', 'omit_front_prior': '5', 'time_field': 'time', 'time_window': False, 'use_interpolation': 'True', 'use_real_time_and_c_rate_transform': 'True', 'use_time_log10_scaling': 'True', 'use_value_normalization': 'True', 'value_field': 'NE', 'directory': 'static/uploads/', 'generation_time_path': 'data/generation_lengths/', 'exclude_subdirs': [], 'use_plotting_on_log10_scale': False, 'sep': '\t'}


m_obj_base = Msmc_clustering(**non_user_settings)
print(m_obj_base.manual_cluster_count, type(m_obj_base.manual_cluster_count))
print(m_obj_base.mySeries)
# m_obj_user = Msmc_clustering(**user_settings)
print(m_obj_base.mySeries)
