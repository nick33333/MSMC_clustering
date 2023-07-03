import MSMC_clustering
from MSMC_clustering import Msmc_clustering
import pandas as pd
import numpy as np
import pickle
import json
import os
import sys



mu_dict = {'bird':1.4e-9,
          'mammal':2.2e-9}
time_series_path = '/scratch/nick/MSMC-Curve-Analysis/msmc_curve_data/'
test_case_path = '/scratch/nick/MSMC-Curve-Analysis/test_case_data/'
generation_lengths_path = '/scratch/nick/MSMC-Curve-Analysis/generation_lengths/'

m_obj = Msmc_clustering(directory=time_series_path,
                        mu=1.4e-9,
                        generation_time_path=generation_lengths_path,
                        real_time=False,
                        normalize_lambda=True,
                        log_scale_time=False,
                        plot_on_log_scale=False,
                        uniform_ts_curve_domains=False,
                        to_omit=[],
                        exclude_subdirs=['mammals_part_1'],
                        manual_cluster_count=7,
                        algo='kmeans',
                        suffix='.txt',
                        omit_front_prior=0,
                        omit_back_prior=0,
                        time_window=False,
                        index_field='time_index',
                        time_field='left_time_boundary',
                        value_field='lambda',
                        ignore_fields= ['right_time_boundary'],
                        sep='\t')


size_estimate = len(pickle.dumps(m_obj))

print(size_estimate)