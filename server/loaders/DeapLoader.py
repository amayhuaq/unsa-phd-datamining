import cPickle

"""
data	40 x 40 x 8064	video/trial x channel x data
labels	40 x 4	        video/trial x label (valence, arousal, dominance, liking)
* Valence	The valence rating (float between 1 and 9).
* Arousal	The arousal rating (float between 1 and 9).
"""


def load_channels():
    channels = [
        {'id': 0, 'label': 'Fp1'},
        {'id': 1, 'label': 'AF3'},
        {'id': 2, 'label': 'F3'},
        {'id': 3, 'label': 'F7'},
        {'id': 4, 'label': 'FC5'},
        {'id': 5, 'label': 'FC1'},
        {'id': 6, 'label': 'C3'},
        {'id': 7, 'label': 'T7'},
        {'id': 8, 'label': 'CP5'},
        {'id': 9, 'label': 'CP1'},
        {'id': 10, 'label': 'P3'},
        {'id': 11, 'label': 'P7'},
        {'id': 12, 'label': 'PO3'},
        {'id': 13, 'label': 'O1'},
        {'id': 14, 'label': 'Oz'},
        {'id': 15, 'label': 'Pz'},
        {'id': 16, 'label': 'Fp2'},
        {'id': 17, 'label': 'AF4'},
        {'id': 18, 'label': 'Fz'},
        {'id': 19, 'label': 'F4'},
        {'id': 20, 'label': 'F8'},
        {'id': 21, 'label': 'FC6'},
        {'id': 22, 'label': 'FC2'},
        {'id': 23, 'label': 'Cz'},
        {'id': 24, 'label': 'C4'},
        {'id': 25, 'label': 'T8'},
        {'id': 26, 'label': 'CP6'},
        {'id': 27, 'label': 'CP2'},
        {'id': 28, 'label': 'P4'},
        {'id': 29, 'label': 'P8'},
        {'id': 30, 'label': 'PO4'},
        {'id': 31, 'label': 'O2'},
        {'id': 32, 'label': 'hEOG'},
        {'id': 33, 'label': 'vEOG'},
        {'id': 34, 'label': 'zEMG'},
        {'id': 35, 'label': 'tEMG'},
        {'id': 36, 'label': 'GSR'},
        {'id': 37, 'label': 'Respiration'},
        {'id': 38, 'label': 'Plethysmograph'},
        {'id': 39, 'label': 'Temperature'}
    ]
    return channels


def format_subject(i, x):
    cls = [{'valence': lab[0], 'arousal': lab[1]} for lab in x['labels'][0:10, :]]
    info = [{'id': 's' + str(i) + '_v' + str(vi)} for vi in range(1, 11)]
    channels = x['data'][0:10, :].tolist()
    return cls, info, channels


def load_dataset(path_db):
    data = {
        'class_or': [],
        'data': [],
        'subjects': []
    }
    for i in range(1, 10):
        x = cPickle.load(open(path_db + 's0' + str(i) + '.dat', 'rb'))
        cls, info, channels = format_subject(i, x)
        data['class_or'] = data['class_or'] + cls
        data['subjects'] = data['subjects'] + info
        data['data'] = data['data'] + channels

    for i in range(10, 33):
        x = cPickle.load(open(path_db + 's' + str(i) + '.dat', 'rb'))
        cls, info, channels = format_subject(i, x)
        data['class_or'] = data['class_or'] + cls
        data['subjects'] = data['subjects'] + info
        data['data'] = data['data'] + channels

    return data
