"""
Based on the paper titled "Emotion Classification in Arousal Valence Model using MAHNOB-HCI Database"
Link: https://pdfs.semanticscholar.org/3750/b635d455fee489305b24ead4b7e9233b7209.pdf
"""

emotions = {
    4: ['LA-PV', 'LA-NV', 'HA-NV', 'HA-PV'],
    9: ['Undefined', 'Happiness', 'Amusement', 'Sadness', 'Disgust', 'Anxiety', 'Fear', 'Surprise', 'Anger', 'Neutral']
}


def discretize(labels, nClasses=4):
    if nClasses == 4:
        for i in range(len(labels)):
            if labels[i]['valence'] >= 5 and labels[i]['arousal'] >= 5:
                labels[i]['emotion'] = 0    # Low Arousal, Positive Valence
            elif labels[i]['valence'] < 5 and labels[i]['arousal'] >= 5:
                labels[i]['emotion'] = 1    # Low Arousal, Negative Valence
            elif labels[i]['valence'] < 5 and labels[i]['arousal'] < 5:
                labels[i]['emotion'] = 2    # High Arousal, Negative Valence
            else:
                labels[i]['emotion'] = 3    # High Arousal, Positive Valence
    elif nClasses == 9:
        """
        (0) Undefined (1) Happiness, (2) Amusement, (3) Sadness, (4) Disgust, (5) Anxiety, (6) Fear, (7) Surprise, (8) Anger, and (9) Neutral
        """
        for i in range(0, len(labels)):
            if labels[i]['arousal'] >= 1 and labels[i]['arousal'] <= 3:  # Calm
                if labels[i]['valence'] >= 1 and labels[i]['valence'] <= 3:  # Unpleasant
                    labels[i]['emotion'] = 3
                elif labels[i]['valence'] >= 4 and labels[i]['valence'] <= 6:  # Neutral
                    labels[i]['emotion'] = 9
                elif labels[i]['valence'] >= 7 and labels[i]['valence'] <= 9:  # Pleasant
                    labels[i]['emotion'] = 0
            elif labels[i]['arousal'] >= 4 and labels[i]['arousal'] <= 6:  # Medium
                if labels[i]['valence'] >= 1 and labels[i]['valence'] <= 3:  # Unpleasant
                    labels[i]['emotion'] = 0
                elif labels[i]['valence'] >= 4 and labels[i]['valence'] <= 6:  # Neutral
                    labels[i]['emotion'] = 0
                elif labels[i]['valence'] >= 7 and labels[i]['valence'] <= 9:  # Pleasant
                    labels[i]['emotion'] = 1
            elif labels[i]['arousal'] >= 7 and labels[i]['arousal'] <= 9:  # Excited
                if labels[i]['valence'] >= 1 and labels[i]['valence'] <= 3:  # Unpleasant
                    labels[i]['emotion'] = 5
                elif labels[i]['valence'] >= 4 and labels[i]['valence'] <= 6:  # Neutral
                    labels[i]['emotion'] = 7
                elif labels[i]['valence'] >= 7 and labels[i]['valence'] <= 9:  # Pleasant
                    labels[i]['emotion'] = 0
    return labels, emotions[nClasses]
