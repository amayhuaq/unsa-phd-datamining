# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 14:39:31 2018

@author: jinyu
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold
import pickle 
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


def eeg_mean_(df):
    return df.mean(axis=1)

def eeg_median_(df):
    return df.median(axis=1)

def eeg_std_(df):
    return df.std(axis=1)

def eeg_min_(df):
    return df.min(axis=1)

def eeg_max_(df):
    return df.max(axis=1)

def eeg_range_(df_max,df_min,eeg_CH):
    return df_max['{}eeg_max'.format(eeg_CH)]-df_min['{}eeg_min'.format(eeg_CH)]

#最小值比率 = Mmin/N
def eeg_minRatio_(all_df,eeg_min,eeg_CH):
    all_df_T = all_df.T
    eeg_min_T = eeg_min.T
    eeg_minRatio_dict = {}
    for i in all_df.index.tolist():
        num_min = len( all_df_T[i][ all_df_T[i] == eeg_min_T.at['{}eeg_min'.format(eeg_CH),i]] )
        eeg_minRatio_dict.update({i:num_min/8064.0})
    eeg_minRatio_df = pd.DataFrame.from_dict(data=eeg_minRatio_dict,orient='index')
    eeg_minRatio_df.columns = ['{}eeg_minRatio'.format(eeg_CH)]
    return eeg_minRatio_df

#最大值比率 = Nmax/N
def eeg_maxRatio_(all_df,eeg_max,eeg_CH):
    all_df_T = all_df.T
    eeg_max_T = eeg_max.T
    eeg_maxRatio_dict = {}
    for i in all_df.index.tolist():
        num_max = len( all_df_T[i][ all_df_T[i] == eeg_max_T.at['{}eeg_max'.format(eeg_CH),i]] )
        eeg_maxRatio_dict.update({i:num_max/8064.0})
    eeg_maxRatio_df = pd.DataFrame.from_dict(data=eeg_maxRatio_dict,orient='index')
    eeg_maxRatio_df.columns = ['{}eeg_maxRatio'.format(eeg_CH)]
    return eeg_maxRatio_df

#EEG一阶差分均值
def eeg1Diff_mean_(all_df):
    eeg1Diff_mean = all_df.diff(periods=1,axis=1).dropna(axis=1).mean(axis=1)
    return eeg1Diff_mean

#EEG一阶差分中值
def eeg1Diff_median_(all_df):
    eeg1Diff_median = all_df.diff(periods=1,axis=1).dropna(axis=1).median(axis=1)
    return eeg1Diff_median

#EEG一阶差分标准差
def eeg1Diff_std_(all_df):
    eeg1Diff_std = all_df.diff(periods=1,axis=1).dropna(axis=1).std(axis=1)
    return eeg1Diff_std

def eeg1Diff_min_(all_df):
    eeg1Diff_min = all_df.diff(periods=1,axis=1).dropna(axis=1).min(axis=1)
    return eeg1Diff_min

def eeg1Diff_max_(all_df):
    eeg1Diff_max = all_df.diff(periods=1,axis=1).dropna(axis=1).max(axis=1)
    return eeg1Diff_max

def eeg1Diff_range_(eeg1Diff_max,eeg1Diff_min,eeg_CH):
    return eeg1Diff_max['{}eeg1Diff_max'.format(eeg_CH)]-eeg1Diff_min['{}eeg1Diff_min'.format(eeg_CH)]

def eeg1Diff_minRatio_(all_df,eeg1Diff_min,eeg_CH):
    all_df_Diff_T = all_df.diff(periods=1,axis=1).dropna(axis=1).T
    eeg1Diff_min_T = eeg1Diff_min.T
    eeg1Diff_minRatio_dict = {}
    for i in all_df.index.tolist():
        num_min = len( all_df_Diff_T[i][ all_df_Diff_T[i] == eeg1Diff_min_T.at['{}eeg1Diff_min'.format(eeg_CH),i]])
        eeg1Diff_minRatio_dict.update({i:num_min/8063.0})
    eeg1Diff_minRatio_df = pd.DataFrame.from_dict(data=eeg1Diff_minRatio_dict,orient='index')
    return eeg1Diff_minRatio_df

def eeg1Diff_maxRatio_(all_df,eeg1Diff_max,eeg_CH):
    all_df_Diff_T = all_df.diff(periods=1,axis=1).dropna(axis=1).T
    eeg1Diff_max_T = eeg1Diff_max.T
    eeg1Diff_maxRatio_dict = {}
    for i in all_df.index.tolist():
        num_max = len( all_df_Diff_T[i][all_df_Diff_T[i] == eeg1Diff_max_T.at['{}eeg1Diff_max'.format(eeg_CH),i]])
        eeg1Diff_maxRatio_dict.update({i:num_max/8063.0})
    eeg1Diff_maxRatio_df = pd.DataFrame.from_dict(data=eeg1Diff_maxRatio_dict,orient='index')
    return eeg1Diff_maxRatio_df

def eeg2Diff_std_(all_df):
    eeg2Diff_std = all_df.diff(periods=2,axis=1).dropna(axis=1).std(axis=1)
    return eeg2Diff_std

def eeg2Diff_min_(all_df):
    eeg2Diff_min = all_df.diff(periods=2,axis=1).dropna(axis=1).min(axis=1)
    return eeg2Diff_min

def eeg2Diff_max_(all_df):
    eeg2Diff_max = all_df.diff(periods=2,axis=1).dropna(axis=1).max(axis=1)
    return eeg2Diff_max

def eeg2Diff_range_(eeg2Diff_max,eeg2Diff_min,eeg_CH):
    eeg2Diff_range = eeg2Diff_max['{}eeg2Diff_max'.format(eeg_CH)]-eeg2Diff_min['{}eeg2Diff_min'.format(eeg_CH)]
    return eeg2Diff_range

def eeg2Diff_minRatio_(all_df,eeg2Diff_min,eeg_CH):
    all_df_2Diff_T = all_df.diff(periods=2,axis=1).dropna(axis=1).T
    eeg2Diff_min_T = eeg2Diff_min.T
    eeg2Diff_minRatio_dict = {}
    for i in all_df.index.tolist():
        num_min = len( all_df_2Diff_T[i][all_df_2Diff_T[i] == eeg2Diff_min_T.at['{}eeg2Diff_min'.format(eeg_CH),i]] )
        eeg2Diff_minRatio_dict.update({i:num_min/8062.0})
    eeg2Diff_minRatio_df = pd.DataFrame.from_dict(data=eeg2Diff_minRatio_dict,orient='index')
    return eeg2Diff_minRatio_df

def eeg2Diff_maxRatio_(all_df,eeg2Diff_max,eeg_CH):
    all_df_2Diff_T = all_df.diff(periods=2,axis=1).dropna(axis=1).T
    eeg2Diff_max_T = eeg2Diff_max.T
    eeg2Diff_maxRatio_dict = {}
    for i in all_df.index.tolist():
        num_max = len( all_df_2Diff_T[i][all_df_2Diff_T[i] == eeg2Diff_max_T.at['{}eeg2Diff_max'.format(eeg_CH),i]] )
        eeg2Diff_maxRatio_dict.update({i:num_max/8062.0})
    eeg2Diff_maxRatio_df = pd.DataFrame.from_dict(data=eeg2Diff_maxRatio_dict,orient='index')
    return eeg2Diff_maxRatio_df

#EEG DFT(FFT)频域数据
def eegfft_(df_data):
    eegfft_df = pd.DataFrame()
    for i in df_data.index.tolist():
        temp_eegfft = pd.DataFrame(np.fft.fft(df_data.loc[i,:].values)).T
        temp_eegfft.index = [i]
        eegfft_df = eegfft_df.append(temp_eegfft)
    return eegfft_df

#EEG 频域中值
def eegfft_mean_(eegfft_df):
    eegfft_mean = eegfft_df.mean(axis=1)
    return eegfft_mean

def eegfft_median_(eegfft_df):
    eegfft_median = eegfft_df.median(axis=1)
    return eegfft_median

def eegfft_std_(eegfft_df):
    eegfft_std = eegfft_df.std(axis=1)
    return eegfft_std

def eegfft_min_(eegfft_df):
    eegfft_min = eegfft_df.min(axis=1)
    return eegfft_min

def eegfft_max_(eegfft_df):
    eegfft_max = eegfft_df.max(axis=1)
    return eegfft_max

def eegfft_range_(eegfft_max,eegfft_min,eeg_CH):
    eegfft_range = eegfft_max['{}eegfft_max'.format(eeg_CH)]-eegfft_min['{}eegfft_min'.format(eeg_CH)]
    return eegfft_range


def extract_features(data_folder, filename, ini, end):
    df_data_x = pickle.load(open(data_folder + filename, "rb"))
    _, sig_sz = df_data_x.shape
    df_data_x = df_data_x[range(ini, min(end, sig_sz))]
    tmp = filename.split('_')
    eeg_CH = tmp[0] + "_" + tmp[1] + "_"

    eeg_mean = pd.DataFrame(eeg_mean_(df_data_x), columns=['{}eeg_mean'.format(eeg_CH)])
    eeg_median = pd.DataFrame(eeg_median_(df_data_x), columns=['{}eeg_median'.format(eeg_CH)])
    eeg_std = pd.DataFrame(eeg_std_(df_data_x), columns=['{}eeg_std'.format(eeg_CH)])
    eeg_min = pd.DataFrame(eeg_min_(df_data_x), columns=['{}eeg_min'.format(eeg_CH)])
    eeg_max = pd.DataFrame(eeg_max_(df_data_x), columns=['{}eeg_max'.format(eeg_CH)])
    eeg_range = pd.DataFrame(eeg_range_(eeg_max,eeg_min,eeg_CH), columns=['{}eeg_range'.format(eeg_CH)])
    eeg_minRatio = pd.DataFrame(eeg_minRatio_(df_data_x,eeg_min,eeg_CH), columns=['{}eeg_minRatio'.format(eeg_CH)])
    eeg_maxRatio = pd.DataFrame(eeg_maxRatio_(df_data_x,eeg_max,eeg_CH), columns=['{}eeg_maxRatio'.format(eeg_CH)])

    eeg1Diff_mean = pd.DataFrame( eeg1Diff_mean_(df_data_x), columns=['{}eeg1Diff_mean'.format(eeg_CH)])
    eeg1Diff_median = pd.DataFrame( eeg1Diff_median_(df_data_x), columns=['{}eeg1Diff_median'.format(eeg_CH)] )
    eeg1Diff_std = pd.DataFrame( eeg1Diff_std_(df_data_x), columns=['{}eeg1Diff_std'.format(eeg_CH)])
    eeg1Diff_min = pd.DataFrame( eeg1Diff_min_(df_data_x), columns=['{}eeg1Diff_min'.format(eeg_CH)])
    eeg1Diff_max = pd.DataFrame( eeg1Diff_max_(df_data_x), columns=['{}eeg1Diff_max'.format(eeg_CH)])
    eeg1Diff_range = pd.DataFrame( eeg1Diff_range_(eeg1Diff_max,eeg1Diff_min,eeg_CH), columns=['{}eeg1Diff_range'.format(eeg_CH)])
    eeg1Diff_minRatio = eeg1Diff_minRatio_(df_data_x,eeg1Diff_min,eeg_CH)
    eeg1Diff_minRatio.columns=['{}eeg1Diff_minRatio'.format(eeg_CH)]
    eeg1Diff_maxRatio = eeg1Diff_maxRatio_(df_data_x,eeg1Diff_max,eeg_CH)
    eeg1Diff_maxRatio.columns=['{}eeg1Diff_maxRatio'.format(eeg_CH)]

    eeg2Diff_std = pd.DataFrame( eeg2Diff_std_(df_data_x), columns=['{}eeg2Diff_std'.format(eeg_CH)] )
    eeg2Diff_min = pd.DataFrame( eeg2Diff_min_(df_data_x), columns=['{}eeg2Diff_min'.format(eeg_CH)] )
    eeg2Diff_max = pd.DataFrame( eeg2Diff_max_(df_data_x), columns=['{}eeg2Diff_max'.format(eeg_CH)] )
    eeg2Diff_range = pd.DataFrame(eeg2Diff_range_(eeg2Diff_max,eeg2Diff_min,eeg_CH), columns=['{}eeg2Diff_range'.format(eeg_CH)])
    eeg2Diff_minRatio = eeg2Diff_minRatio_(df_data_x,eeg2Diff_min,eeg_CH)
    eeg2Diff_minRatio.columns=['{}eeg2Diff_minRatio'.format(eeg_CH)]
    eeg2Diff_maxRatio = eeg2Diff_maxRatio_(df_data_x,eeg2Diff_max,eeg_CH)
    eeg2Diff_maxRatio.columns=['{}eeg2Diff_maxRatio'.format(eeg_CH)]

    temp_eegfft = eegfft_(df_data_x)
    locals()["{}eegfft_df".format(eeg_CH)] = temp_eegfft
    eegfft_df = locals()["{}eegfft_df".format(eeg_CH)]

    eegfft_mean = pd.DataFrame( eegfft_mean_(eegfft_df), columns=['{}eegfft_mean'.format(eeg_CH)])
    eegfft_median = pd.DataFrame( eegfft_median_(eegfft_df), columns=['{}eegfft_median'.format(eeg_CH)])
    eegfft_std = pd.DataFrame( eegfft_std_(eegfft_df), columns=['{}eegfft_std'.format(eeg_CH)])
    eegfft_min = pd.DataFrame( eegfft_min_(eegfft_df), columns=['{}eegfft_min'.format(eeg_CH)])
    eegfft_max = pd.DataFrame( eegfft_max_(eegfft_df), columns=['{}eegfft_max'.format(eeg_CH)])
    eegfft_range = pd.DataFrame( eegfft_range_(eegfft_max,eegfft_min,eeg_CH), columns=['{}eegfft_range'.format(eeg_CH)])

    feature_list = ['eeg_mean','eeg_median','eeg_std','eeg_min','eeg_max','eeg_range',
                'eeg_minRatio','eeg_maxRatio','eeg1Diff_mean','eeg1Diff_median',
                'eeg1Diff_std','eeg1Diff_min','eeg1Diff_max','eeg1Diff_range',
                'eeg1Diff_minRatio','eeg1Diff_maxRatio','eeg2Diff_std',
                'eeg2Diff_min','eeg2Diff_max','eeg2Diff_range','eeg2Diff_minRatio',
                'eeg2Diff_maxRatio','eegfft_mean','eegfft_median','eegfft_std',
                'eegfft_min','eegfft_max','eegfft_range']

    temp_feature_df = pd.DataFrame()
    for i in feature_list:
        temp_feature_df = pd.concat([locals()[i], temp_feature_df], axis=1)
    pickle.dump(temp_feature_df, open(data_folder + "feat_" + filename, "wb"))

    print('--- EEG features ---')
    print(temp_feature_df.shape)
    return temp_feature_df
