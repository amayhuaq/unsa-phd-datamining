import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
import server.emovis.EmoDiscretization as EDisc
import server.emoclass.ClassifiersManager as ClfMan
import server.emoclass.FeatureManager as FMan

nClasses = None


def classify_2dim(data, clf_valence, clf_arousal):
    valence = clf_valence.predict(data)
    arousal = clf_arousal.predict(data)
    return [{'valence': valence[i], 'arousal': arousal[i]} for i in range(len(valence))]


def classify_1dim(data, clf):
    pred_vals = clf.predict(data)
    return [EDisc.get_centroid_emotion(pred_vals[i], nClasses) for i in range(len(pred_vals))]


def train_and_test_by_scale(features, all_df_y, id_classifier, test_size):
    n_folds = round(1 / (test_size / 100.0))
    kf = KFold(n_splits=n_folds)
    max_acc_aro = 0
    max_acc_val = 0
    best_clf_val = None
    best_clf_aro = None
    for train_index, test_index in kf.split(features):
        X_train, X_test = features[train_index], features[test_index]
        y_train_v, y_test_v = all_df_y['valence'][train_index], all_df_y['valence'][test_index]
        y_train_a, y_test_a = all_df_y['arousal'][train_index], all_df_y['arousal'][test_index]
        clf_val = ClfMan.train_classifier(id_classifier, X_train, y_train_v, saveClf=False)
        clf_aro = ClfMan.train_classifier(id_classifier, X_train, y_train_a, saveClf=False)
        acc_val = ClfMan.test_classifier(clf_val, X_test, y_test_v)
        acc_aro = ClfMan.test_classifier(clf_val, X_test, y_test_a)
        if acc_val > max_acc_val:
            max_acc_val = acc_val
            best_clf_val = clf_val
        if acc_aro > max_acc_aro:
            max_acc_aro = acc_aro
            best_clf_aro = clf_aro

    predicted_vals = classify_2dim(features, best_clf_val, best_clf_aro)
    return predicted_vals, best_clf_val, best_clf_aro


def train_and_test_by_level(features, all_df_y, id_classifier, test_size):
    n_folds = round(1 / (test_size / 100.0))
    kf = KFold(n_splits=n_folds)
    max_acc_aro = 0
    max_acc_val = 0
    best_clf_val = None
    best_clf_aro = None
    tmp_labs, _ = EDisc.discretize_by_level(all_df_y.to_dict('records'), nClasses)
    all_df_y = pd.DataFrame.from_records(tmp_labs)

    for train_index, test_index in kf.split(features):
        X_train, X_test = features[train_index], features[test_index]
        y_train_v, y_test_v = all_df_y['val_lvl'][train_index], all_df_y['val_lvl'][test_index]
        y_train_a, y_test_a = all_df_y['aro_lvl'][train_index], all_df_y['aro_lvl'][test_index]
        """
        print(np.count_nonzero(np.isnan(X_train)), np.count_nonzero(np.isnan(X_test)))
        print(np.count_nonzero(np.isnan(y_train_v)), np.count_nonzero(np.isnan(y_test_v)))
        print(np.count_nonzero(np.isnan(y_train_a)), np.count_nonzero(np.isnan(y_test_a)))
        """
        clf_val = ClfMan.train_classifier(id_classifier, X_train, y_train_v, saveClf=False)
        clf_aro = ClfMan.train_classifier(id_classifier, X_train, y_train_a, saveClf=False)
        acc_val = ClfMan.test_classifier(clf_val, X_test, y_test_v)
        acc_aro = ClfMan.test_classifier(clf_val, X_test, y_test_a)
        if acc_val > max_acc_val:
            max_acc_val = acc_val
            best_clf_val = clf_val
        if acc_aro > max_acc_aro:
            max_acc_aro = acc_aro
            best_clf_aro = clf_aro

    # predict values for all
    valence = best_clf_val.predict(features)
    arousal = best_clf_aro.predict(features)
    """
    print("testing arousal with all")
    ClfMan.test_classifier(best_clf_aro, features, all_df_y['aro_lvl'])
    ClfMan.test_classifier(best_clf_val, features, all_df_y['val_lvl'])
    """
    predicted_vals = [{'valence': EDisc.get_centroid_level(valence[i], nClasses), 'arousal': EDisc.get_centroid_level(arousal[i], nClasses)} for i in range(len(valence))]
    return predicted_vals, best_clf_val, best_clf_aro


def train_and_test_by_emotion(features, all_df_y, id_classifier, test_size):
    n_folds = round(1 / (test_size / 100.0))
    kf = KFold(n_splits=n_folds)
    max_acc = 0
    best_clf = None
    for train_index, test_index in kf.split(features):
        X_train, X_test = features[train_index], features[test_index]
        y_train, y_test = all_df_y['emotion'][train_index], all_df_y['emotion'][test_index]
        clf_val = ClfMan.train_classifier(id_classifier, X_train, y_train, saveClf=False)
        acc_val = ClfMan.test_classifier(clf_val, X_test, y_test)
        if acc_val > max_acc:
            max_acc = acc_val
            best_clf = clf_val
    predicted_vals = classify_1dim(features, best_clf)
    return predicted_vals, best_clf, None


modeClassification = {
    'AVs': train_and_test_by_scale,
    'AVl': train_and_test_by_level,
    'emo': train_and_test_by_emotion
}


def start_classification(data_in, data_folder):
    global nClasses
    nClasses = data_in["nClasses"]
    features_or = FMan.extract_features(data_in, data_folder)
    features = FMan.select_features(data_in["fselector"], features_or)
    print('fselector', features.shape)
    # training classifiers
    all_df_y = pickle.load(open(data_folder + 'all_df_y', 'rb'))
    tmp_labs, _ = EDisc.discretize(all_df_y.to_dict('records'), nClasses)
    all_df_y = pd.DataFrame.from_records(tmp_labs)
    predicted_vals = None
    if data_in["mode"] in modeClassification.keys():
        predicted_vals, _, _ = modeClassification[data_in["mode"]](features, all_df_y, data_in["classifier"], data_in["testSize"])

    return predicted_vals, all_df_y.to_dict('records'), features_or


if __name__ == "__main__":
    data = {'channels': ['GSR_GSR'], 'winSize': 63, 'winIni': 0, 'sampleSize': 128, 'fselector': "",
            'classifier': "svm", 'nClasses': 9, 'testSize': 20, 'mode': "AVl"}
    out_folder = '../../datasets/data_files/'
    pred, ground, features = start_classification(data, out_folder)
    print(features.shape)
    print(len(pred), len(ground))
    print(pred)
    print(ground)