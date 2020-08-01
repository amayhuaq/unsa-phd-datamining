# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 21:02:45 2018
@author: jinyx
"""

import pandas as pd
import numpy as np
import pickle


def sc_mean_(df):
    return df.mean(axis=1)

def sc_median_(df):
    return df.median(axis=1)

def sc_std_(df):
    return df.std(axis=1)

def sc_min_(df):
    return df.min(axis=1)

def sc_max_(df):
    return df.max(axis=1)

def sc_range_(df_max,df_min):
    return df_max['sc_max']-df_min['sc_min']

#最小值比率 = Mmin/N
def sc_minRatio_(all_df,sc_min):
    all_df_T = all_df.T
    sc_min_T = sc_min.T
    sc_minRatio_dict = {}
    for i in all_df.index.tolist():
        num_min = len( all_df_T[i][ all_df_T[i] == sc_min_T.at['sc_min',i]] )   
        sc_minRatio_dict.update({i:num_min/8064.0})   
    sc_minRatio_df = pd.DataFrame.from_dict(data=sc_minRatio_dict,orient='index')
    sc_minRatio_df.columns = ['sc_minRatio']
    return sc_minRatio_df

#最大值比率 = Nmax/N
def sc_maxRatio_(all_df,sc_max):
    all_df_T = all_df.T
    sc_max_T = sc_max.T
    sc_maxRatio_dict = {}
    for i in all_df.index.tolist():
        num_max = len( all_df_T[i][ all_df_T[i] == sc_max_T.at['sc_max',i]] )   
        sc_maxRatio_dict.update({i:num_max/8064.0})    
    sc_maxRatio_df = pd.DataFrame.from_dict(data=sc_maxRatio_dict,orient='index')
    sc_maxRatio_df.columns = ['sc_maxRatio']
    return sc_maxRatio_df   

#GSR一阶差分均值 
def sc1Diff_mean_(all_df):
    sc1Diff_mean = all_df.diff(periods=1,axis=1).dropna(axis=1).mean(axis=1)    
    return sc1Diff_mean

#GSR一阶差分中值
def sc1Diff_median_(all_df):
    sc1Diff_median = all_df.diff(periods=1,axis=1).dropna(axis=1).median(axis=1)
    return sc1Diff_median

#GSR一阶差分标准差
def sc1Diff_std_(all_df):
    sc1Diff_std = all_df.diff(periods=1,axis=1).dropna(axis=1).std(axis=1)
    return sc1Diff_std

def sc1Diff_min_(all_df):
    sc1Diff_min = all_df.diff(periods=1,axis=1).dropna(axis=1).min(axis=1)
    return sc1Diff_min
    
def sc1Diff_max_(all_df):
    sc1Diff_max = all_df.diff(periods=1,axis=1).dropna(axis=1).max(axis=1)
    return sc1Diff_max    

def sc1Diff_range_(sc1Diff_max,sc1Diff_min):
    return sc1Diff_max['sc1Diff_max']-sc1Diff_min['sc1Diff_min']

def sc1Diff_minRatio_(all_df,sc1Diff_min):
    all_df_Diff_T = all_df.diff(periods=1,axis=1).dropna(axis=1).T
    sc1Diff_min_T = sc1Diff_min.T
    sc1Diff_minRatio_dict = {}
    for i in all_df.index.tolist():
        num_min = len( all_df_Diff_T[i][ all_df_Diff_T[i] == sc1Diff_min_T.at['sc1Diff_min',i]])
        sc1Diff_minRatio_dict.update({i:num_min/8063.0})
    sc1Diff_minRatio_df = pd.DataFrame.from_dict(data=sc1Diff_minRatio_dict,orient='index')
    return sc1Diff_minRatio_df

def sc1Diff_maxRatio_(all_df,sc1Diff_max):
    all_df_Diff_T = all_df.diff(periods=1,axis=1).dropna(axis=1).T
    sc1Diff_max_T = sc1Diff_max.T
    sc1Diff_maxRatio_dict = {}
    for i in all_df.index.tolist():
        num_max = len( all_df_Diff_T[i][all_df_Diff_T[i] == sc1Diff_max_T.at['sc1Diff_max',i]])
        sc1Diff_maxRatio_dict.update({i:num_max/8063.0})
    sc1Diff_maxRatio_df = pd.DataFrame.from_dict(data=sc1Diff_maxRatio_dict,orient='index')
    return sc1Diff_maxRatio_df

def sc2Diff_std_(all_df):
    sc2Diff_std = all_df.diff(periods=2,axis=1).dropna(axis=1).std(axis=1)
    return sc2Diff_std

def sc2Diff_min_(all_df):
    sc2Diff_min = all_df.diff(periods=2,axis=1).dropna(axis=1).min(axis=1)
    return sc2Diff_min

def sc2Diff_max_(all_df):
    sc2Diff_max = all_df.diff(periods=2,axis=1).dropna(axis=1).max(axis=1)
    return sc2Diff_max

def sc2Diff_range_(sc2Diff_max,sc2Diff_min):
    sc2Diff_range = sc2Diff_max['sc2Diff_max']-sc2Diff_min['sc2Diff_min']
    return sc2Diff_range

def sc2Diff_minRatio_(all_df,sc2Diff_min):
    all_df_2Diff_T = all_df.diff(periods=2,axis=1).dropna(axis=1).T
    sc2Diff_min_T = sc2Diff_min.T
    sc2Diff_minRatio_dict = {}
    for i in all_df.index.tolist():
        num_min = len( all_df_2Diff_T[i][all_df_2Diff_T[i] == sc2Diff_min_T.at['sc2Diff_min',i]] )
        sc2Diff_minRatio_dict.update({i:num_min/8062.0})
    sc2Diff_minRatio_df = pd.DataFrame.from_dict(data=sc2Diff_minRatio_dict,orient='index')
    return sc2Diff_minRatio_df
        
def sc2Diff_maxRatio_(all_df,sc2Diff_max):
    all_df_2Diff_T = all_df.diff(periods=2,axis=1).dropna(axis=1).T
    sc2Diff_max_T = sc2Diff_max.T
    sc2Diff_maxRatio_dict = {}
    for i in all_df.index.tolist():
        num_max = len( all_df_2Diff_T[i][all_df_2Diff_T[i] == sc2Diff_max_T.at['sc2Diff_max',i]] )
        sc2Diff_maxRatio_dict.update({i:num_max/8062.0})
    sc2Diff_maxRatio_df = pd.DataFrame.from_dict(data=sc2Diff_maxRatio_dict,orient='index')
    return sc2Diff_maxRatio_df

#GSR DFT(FFT)频域数据
def scfft_(all_df):
    scfft_df = pd.DataFrame()
    for i in all_df.index.tolist():
        temp_scfft = pd.DataFrame(np.fft.fft(all_df.loc[i,:].values)).T
        temp_scfft.index = [i]
        scfft_df = scfft_df.append(temp_scfft)
    return scfft_df
        
#GSR 频域中值
def scfft_mean_(scfft_df):
    scfft_mean = scfft_df.mean(axis=1)
    return scfft_mean

def scfft_median_(scfft_df):
    scfft_median = scfft_df.median(axis=1)
    return scfft_median

def scfft_std_(scfft_df):
    scfft_std = scfft_df.std(axis=1)
    return scfft_std

def scfft_min_(scfft_df):
    scfft_min = scfft_df.min(axis=1)
    return scfft_min

def scfft_max_(scfft_df):
    scfft_max = scfft_df.max(axis=1)
    return scfft_max

def scfft_range_(scfft_max,scfft_min):
    scfft_range = scfft_max['scfft_max']-scfft_min['scfft_min']
    return scfft_range

def get_123count_(df):
    tmp_df =pd.DataFrame()
    for i in range(0,40,1):
        num_1 = len(df[i][ df[i]==1 ])
        num_2 = len(df[i][ df[i]==2 ])
        num_3 = len(df[i][ df[i]==3 ])
        list_num = [num_1,num_2,num_3]
        tmp_df = pd.concat([tmp_df,pd.DataFrame(list_num)],axis=1)  
    tmp_df.columns = range(0,40,1)
    tmp_df.index = ['num_1','num_2','num_3']
    return tmp_df
    

def extract_features(data_folder, file_names, ini, winSize, sample):
    end = ini + winSize * sample
    feature_df = pd.DataFrame()

    for file in file_names:
        all_df_GSR_x = pickle.load(open(data_folder + file, "rb"))
        all_df_GSR_x = all_df_GSR_x[range(ini, end)]

        sc_mean = pd.DataFrame(sc_mean_(all_df_GSR_x), columns=['sc_mean'])
        sc_median = pd.DataFrame(sc_median_(all_df_GSR_x),columns=['sc_median'])
        sc_std = pd.DataFrame(sc_std_(all_df_GSR_x),columns=['sc_std'])
        sc_min = pd.DataFrame(sc_min_(all_df_GSR_x),columns=['sc_min'])
        sc_max = pd.DataFrame(sc_max_(all_df_GSR_x),columns=['sc_max'])
        sc_range = pd.DataFrame(sc_range_(sc_max,sc_min),columns=['sc_range'])
        sc_minRatio = pd.DataFrame(sc_minRatio_(all_df_GSR_x,sc_min),columns=['sc_minRatio'])
        sc_maxRatio = pd.DataFrame(sc_maxRatio_(all_df_GSR_x,sc_max),columns=['sc_maxRatio'])

        sc1Diff_mean = pd.DataFrame( sc1Diff_mean_(all_df_GSR_x),columns=['sc1Diff_mean'])
        sc1Diff_median = pd.DataFrame( sc1Diff_median_(all_df_GSR_x),columns=['sc1Diff_median'] )
        sc1Diff_std = pd.DataFrame( sc1Diff_std_(all_df_GSR_x),columns=['sc1Diff_std'])
        sc1Diff_min = pd.DataFrame( sc1Diff_min_(all_df_GSR_x),columns=['sc1Diff_min'])
        sc1Diff_max = pd.DataFrame( sc1Diff_max_(all_df_GSR_x),columns=['sc1Diff_max'])
        sc1Diff_range = pd.DataFrame( sc1Diff_range_(sc1Diff_max,sc1Diff_min),columns=['sc1Diff_range'])
        sc1Diff_minRatio = sc1Diff_minRatio_(all_df_GSR_x,sc1Diff_min)
        sc1Diff_minRatio.columns=['sc1Diff_minRatio']
        sc1Diff_maxRatio = sc1Diff_maxRatio_(all_df_GSR_x,sc1Diff_max)
        sc1Diff_maxRatio.columns=['sc1Diff_maxRatio']

        sc2Diff_std = pd.DataFrame( sc2Diff_std_(all_df_GSR_x),columns=['sc2Diff_std'] )
        sc2Diff_min = pd.DataFrame( sc2Diff_min_(all_df_GSR_x),columns=['sc2Diff_min'] )
        sc2Diff_max = pd.DataFrame( sc2Diff_max_(all_df_GSR_x),columns=['sc2Diff_max'] )
        sc2Diff_range = pd.DataFrame(sc2Diff_range_(sc2Diff_max,sc2Diff_min),columns=['sc2Diff_range'])
        sc2Diff_minRatio = sc2Diff_minRatio_(all_df_GSR_x,sc2Diff_min)
        sc2Diff_minRatio.columns = ['sc2Diff_minRatio']
        sc2Diff_maxRatio = sc2Diff_maxRatio_(all_df_GSR_x,sc2Diff_max)
        sc2Diff_maxRatio.columns = ['sc2Diff_maxRatio']

        scfft_df = scfft_(all_df_GSR_x)
        scfft_mean = pd.DataFrame( scfft_mean_(scfft_df),columns=['scfft_mean'])
        scfft_median = pd.DataFrame( scfft_median_(scfft_df),columns=['scfft_median'])
        scfft_std = pd.DataFrame( scfft_std_(scfft_df),columns=['scfft_std'])
        scfft_min = pd.DataFrame( scfft_min_(scfft_df),columns=['scfft_min'])
        scfft_max = pd.DataFrame( scfft_max_(scfft_df),columns=['scfft_max'])
        scfft_range = pd.DataFrame( scfft_range_(scfft_max,scfft_min),columns=['scfft_range'])

        feature_list = ['sc_mean','sc_median','sc_std','sc_min','sc_max','sc_range',
                        'sc_minRatio','sc_maxRatio','sc1Diff_mean','sc1Diff_median',
                        'sc1Diff_std','sc1Diff_min','sc1Diff_max','sc1Diff_range',
                        'sc1Diff_minRatio','sc1Diff_maxRatio','sc2Diff_std',
                        'sc2Diff_min','sc2Diff_max','sc2Diff_range','sc2Diff_minRatio',
                        'sc2Diff_maxRatio','scfft_mean','scfft_median','scfft_std',
                        'scfft_min','scfft_max','scfft_range']

        temp_feature_df = pd.DataFrame()
        for i in feature_list:
            temp_feature_df = pd.concat([locals()[i], temp_feature_df], axis=1)
        pickle.dump(temp_feature_df, open(data_folder + "feat_" + file, "wb"))
        feature_df = pd.concat([feature_df, temp_feature_df], axis=1)

    print('--- GSR features ---')
    print(feature_df.shape)
    return feature_df
