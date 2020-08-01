import pandas as pd
import numpy as np
import os
import re
import pickle
import server.emoclass.ClassifiersManager as clfman
import server.features.GSR_feature_extract as gsr_fex
import server.features.EEG_feature_extract as eeg_fex
import server.features.RSP_feature_extract as rsp_fex

isOnline = False

featureExtractor = {
    'EEG': eeg_fex.extract_features,
    #'EOG': None,
    #'EMG': None,
    'GSR': gsr_fex.extract_features,
    'RESP': rsp_fex.extract_features
    #'BVP': None,
    #'TEMP': None,
}


def processSignal(data):
    return 0


def extractFeatures(dataIn, data_folder):
    selectedSignals = dataIn["signals"]
    winSize = dataIn["winSize"]
    winIni = dataIn["winIni"]
    sampleSize = dataIn["sampleSize"]
    if isOnline:
        for signal in selectedSignals:
            if signal in featureExtractor.keys():
                pattern = re.compile("^" + signal)
                file_names = [f for f in os.listdir(data_folder) if pattern.match(f)]
                featureExtractor[signal](data_folder, file_names, winIni, winSize, sampleSize)

    features_df = pd.DataFrame()
    pattern = re.compile("^feat_")
    file_names = [f for f in os.listdir(data_folder) if pattern.match(f)]
    for fname in file_names:
        temp_features_df = pickle.load(open(data_folder + fname, 'rb'))
        features_df = pd.concat([features_df, temp_features_df], axis=1)

    # remove complex
    df_abs = features_df.select_dtypes(["complex128"]).apply(np.abs)
    list_drop = df_abs.columns
    features_df.drop(labels=list_drop, axis=1, inplace=True)
    features_df = pd.concat([df_abs, features_df], axis=1)

    features_df = features_df.fillna(0)
    pickle.dump(features_df, open(data_folder + "all_features_x", "wb"))
    return features_df


def selectFeatures(data):
    return 0


def classify(data, clf_valence, clf_arousal):
    valence = clf_valence.predict(data)
    arousal = clf_arousal.predict(data)
    return [{'valence': valence[i], 'arousal': arousal[i]} for i in range(len(valence))]


def initProcess(dataIn, models_folder, data_folder):
    # extract features
    features = extractFeatures(dataIn, data_folder)

    # load models
    clf_valence = clfman.load_classifier(models_folder, dataIn['classifier'] + '_valence')
    clf_arousal = clfman.load_classifier(models_folder, dataIn['classifier'] + '_arousal')

    # classify
    classes = classify(features, clf_valence, clf_arousal)
    feature_names = features.columns.tolist()

    return features, classes, feature_names


if __name__ == "__main__":
    data = {'signals': ['GSR', 'EEG', 'RESP'], 'winSize': 63, 'winIni': 0, 'sampleSize': 128}
    extractFeatures(data, '../../datasets/data_files/')