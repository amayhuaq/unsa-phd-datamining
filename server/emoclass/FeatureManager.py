import pandas as pd
import numpy as np
import pickle
import server.features.GSR_feature_extract as gsr_fex
import server.features.EEG_feature_extract as eeg_fex
import server.features.RSP_feature_extract as rsp_fex
from sklearn import decomposition


featureExtractor = {
    'EEG': eeg_fex.extract_features,
    #'EOG': None,
    #'EMG': None,
    'GSR': gsr_fex.extract_features,
    'RESP': rsp_fex.extract_features
    #'BVP': None,
    #'TEMP': None,
}

featureSelector = {
    'pca': decomposition.PCA(n_components='mle')
}


def get_original_features(data_folder):
    df_data = pickle.load(open(data_folder + "all_features_x", "rb"))
    return df_data


def extract_features(data_in, data_folder):
    selected_chs = data_in["channels"]
    win_size = data_in["winSize"]
    win_ini = data_in["winIni"]
    sample_size = data_in["sampleSize"]
    win_end = win_ini + win_size * sample_size
    features_df = pd.DataFrame()

    for sig_ch in selected_chs:
        signal, channel = sig_ch.split('_')
        if signal in featureExtractor.keys():
            tmp_df = featureExtractor[signal](data_folder, sig_ch + '_df_x', win_ini, win_end)
            features_df = pd.concat([features_df, tmp_df], axis=1)

    # remove complex
    df_abs = features_df.select_dtypes(["complex128"]).apply(np.abs)
    list_drop = df_abs.columns
    features_df.drop(labels=list_drop, axis=1, inplace=True)
    features_df = pd.concat([df_abs, features_df], axis=1)
    # refill NaN values with the average
    features_df = features_df.fillna(features_df.mean())
    pickle.dump(features_df, open(data_folder + "all_features_x", "wb"))
    print("final features", features_df.shape)
    return features_df


def select_features(fselector, features):
    if fselector in featureSelector.keys():
        tech = featureSelector[fselector]
        tech.fit(features)
        features = tech.transform(features)
    else:
        features = features.values
    return features


if __name__ == "__main__":
    data = {'channels': ['GSR_GSR', 'EEG_P8', 'RESP_Respiration'], 'winSize': 63, 'winIni': 0, 'sampleSize': 128}
    out_folder = '../../datasets/data_files/'
    """
    tmp_df = extract_features(data, out_folder)
    print("previous features: ", tmp_df.shape)
    new_feat = select_features('pca', tmp_df)
    print("selected features", new_feat.shape)
    """
    features = get_original_features(out_folder)
    print(features.shape)
