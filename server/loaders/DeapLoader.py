import _pickle
import pandas as pd
import os

"""
data	40 x 40 x 8064	video/trial x channel x data
labels	40 x 4	        video/trial x label (valence, arousal, dominance, liking)
* Valence	The valence rating (float between 1 and 9).
* Arousal	The arousal rating (float between 1 and 9).
"""

signalData = {
    'EEG': { 'channels': ['Fp1', 'AF3', 'F3', 'F7', 'FC5', 'FC1', 'C3', 'T7', 'CP5', 'CP1', 'P3', 'P7', 'PO3', 'O1',
                          'Oz', 'Pz', 'Fp2', 'AF4', 'Fz', 'F4', 'F8', 'FC6', 'FC2', 'Cz', 'C4', 'T8', 'CP6', 'CP2',
                          'P4', 'P8', 'PO4', 'O2'],
             'ini': 0 },
    'EOG': { 'channels': ['hEOG', 'vEOG'], 'ini': 32 },
    'EMG': { 'channels': ['zEMG', 'tEMG'], 'ini': 34 },
    'GSR': { 'channels': ['GSR'], 'ini': 36 },
    'RESP': { 'channels': ['Respiration'], 'ini': 37 },
    'BVP': {'channels': ['Plethysmograph'], 'ini': 38},
    'TEMP': {'channels': ['Temperature'], 'ini': 39},
}

subjects = ['s01', 's02', 's03', 's04', 's05', 's06', 's07', 's08', 's09', 's10',
            's11', 's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20',
            's21', 's22', 's23', 's24', 's25', 's26', 's27', 's28', 's29', 's30',
            's31', 's32']


def load_signals(folder_path):
    return signalData


def format_subject(i, x):
    cls = [{'valence': lab[0], 'arousal': lab[1]} for lab in x['labels'][0:10, :]]
    info = [{'id': 's' + str(i) + '_v' + str(vi)} for vi in range(1, 11)]
    channels = x['data'][0:10, :].tolist()
    return cls, info, channels


def convert_dataset(path_db, output_folder):
    all_df_y = pd.DataFrame()
    channels_df_x = {}
    for subj in subjects:
        print("Loading " + subj + " data ...")
        sXX = _pickle.load(open(path_db + subj + '.dat', 'rb'), encoding='latin1')

        # save labels
        sXX_df = pd.DataFrame(sXX['labels'][:, 0:2])
        sXX_df = sXX_df.round(0)
        sXX_df.columns = ['valence', 'arousal']
        temp_index = []
        for j in range(40):
            temp_index.append(subj + '_' + str(j))
        sXX_df.index = temp_index
        all_df_y = pd.concat([all_df_y, sXX_df])

        # save channels
        for signal in signalData:
            ch_ini = signalData[signal]['ini']
            ch_end = ch_ini + len(signalData[signal]['channels'])
            for ch in range(ch_ini, ch_end):
                channel_df = pd.DataFrame(sXX['data'][:, ch, :])
                channel_df.index = temp_index
                idCh = signal + "_CH" + str(ch) + "_df_x"
                if idCh not in channels_df_x:
                    channels_df_x[idCh] = pd.DataFrame()
                channels_df_x[idCh] = pd.concat([channels_df_x[idCh], channel_df])

    _pickle.dump(all_df_y, open(output_folder + "all_df_y", "wb"))
    for fname in channels_df_x:
        _pickle.dump(channels_df_x[fname], open(output_folder + fname, "wb"))


if __name__ == "__main__":
    convert_dataset('../../datasets/deap_preprocessed/', '../../datasets/data_files/')
    data = _pickle.load(open('../../datasets/data_files/all_df_y', 'rb'))
    print(data)
