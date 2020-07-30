def discretize(labels):
    for i in range(0, len(labels)):
        if labels[i]['valence'] > 5 and labels[i]['arousal'] > 5:
            labels[i]['emotion'] = "Q1"
        elif labels[i]['valence'] < 5 and labels[i]['arousal'] > 5:
            labels[i]['emotion'] = "Q2"
        elif labels[i]['valence'] < 5 and labels[i]['arousal'] < 5:
            labels[i]['emotion'] = "Q3"
        else:
            labels[i]['emotion'] = "Q4"
    return labels