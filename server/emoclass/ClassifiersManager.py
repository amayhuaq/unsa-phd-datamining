import numpy as np
import pickle
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn import svm, datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from joblib import dump, load

classifiers = {
    'lda': LinearDiscriminantAnalysis(),
    'qda': QuadraticDiscriminantAnalysis(),
    'rf': RandomForestClassifier(n_estimators=100, max_depth=5, oob_score=True, min_samples_split=20),
    'ab': AdaBoostClassifier(n_estimators=100),
    'knn': KNeighborsClassifier(n_neighbors=9),
    'svm': svm.SVC()
}


def evaluator(classifier, ypred, ytest):
    errors = abs(ypred - ytest)
    val = np.count_nonzero(errors)
    print('=== Classifier: ' + classifier + ' ===')
    #print("M A E: ", np.mean(errors))
    print(np.count_nonzero(errors), len(ytest))
    print('Accuracy: ', accuracy_score(ytest, ypred))
    

def train_classifier(idClassifier,  Xtrain, ytrain, saveClf=True, nameClf='', folder=''):
    clf = classifiers[idClassifier]
    clf.fit(Xtrain, ytrain)
    if saveClf:
        if nameClf == '':
            nameClf = idClassifier
        dump(clf, folder + nameClf + '.joblib')
    return clf


def test_classifier(clf, Xtest, ytest):
    ypred = clf.predict(Xtest)
    errors = abs(ypred - ytest)
    print('Errors: ', str(np.count_nonzero(errors)) + ' / ' + str(len(ytest)))
    acc = accuracy_score(ytest, ypred)
    print('Accuracy: ', acc)
    return acc


def load_classifier(folder, nameClf):
    return load(folder + nameClf + '.joblib')


if __name__ == "__main__":
    folder = '../models/'
    data_folder = '../../datasets/data_files/'
    y = pickle.load(open('../../datasets/data_files/all_df_y', 'rb'))
    X = pickle.load(open('../../datasets/data_files/all_features_x', 'rb'))
    print(X.shape, y.shape)

    idClf = 'knn'
    train_classifier(idClf, X.values.tolist(), y['valence'].values.tolist(), folder=folder, nameClf=idClf + '_valence')
    train_classifier(idClf, X.values.tolist(), y['arousal'].values.tolist(), folder=folder, nameClf=idClf + '_arousal')
    clf = load_classifier(folder, idClf + '_valence')
    test_classifier(clf, X, y['valence'])
    print(clf.predict(X[0:3]))
    clf = load_classifier(folder, idClf + '_arousal')
    test_classifier(clf, X, y['arousal'])
    print(clf.predict(X[0:3]))
