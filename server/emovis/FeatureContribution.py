import numpy as np
from ccpca import CCPCA


def simplify(feat_mat, emotion_names, feature_names, nFeatures=15):
    print('max-val', feat_mat.max())
    print('min-val', feat_mat.min())

    nFeat, nEmos = feat_mat.shape
    idFeat = []
    for i in range(nEmos):
        tmp = np.abs(feat_mat[:, i])
        tmp = np.argpartition(tmp, -nFeatures)[-nFeatures:]
        idFeat = idFeat + tmp.tolist()
    print(idFeat)
    print(type(idFeat))

    idFeat = np.unique(idFeat)
    feat_mat_final = np.zeros((len(idFeat), nEmos))
    fnames = []
    pos = 0
    print('len: ', len(idFeat))
    for i in idFeat:
        feat_mat_final[pos, :] = feat_mat[i, :]
        fnames.append(feature_names[i])
        pos = pos + 1

    print('max-val', feat_mat_final.max())
    print('min-val', feat_mat_final.min())
    print(feat_mat_final.tolist())
    return np.asmatrix(feat_mat_final).tolist(), emotion_names, fnames


def computeContribution(features, labels, emotion_names, feature_names):
    y = np.array([cls['emotion'] for cls in labels])
    unique_labels = np.unique(y)
    _, n_feats = features.shape
    n_labels = len(unique_labels)
    first_cpc_mat = np.zeros((n_feats, n_labels))
    feat_contrib_mat = np.zeros((n_feats, n_labels))

    # 1. get the scaled feature contributions and first cPC for each label
    ccpca = CCPCA(n_components=1)
    for i, target_label in enumerate(unique_labels):
        ccpca.fit(
            features[y == target_label],
            features[y != target_label],
            var_thres_ratio=0.5,
            n_alphas=40,
            max_log_alpha=0.5)

        first_cpc_mat[:, i] = ccpca.get_first_component()
        feat_contrib_mat[:, i] = ccpca.get_scaled_feat_contribs()

    """
    # 2. apply optimal sign flipping
    OptSignFlip().opt_sign_flip(first_cpc_mat, feat_contrib_mat)

    # 3. apply hierarchical clustering with optimal-leaf-ordering
    mr = MatReorder()
    mr.fit_transform(feat_contrib_mat)

    # 4. apply aggregation
    n_feats_shown = 25
    agg_feat_contrib_mat, label_to_rows, label_to_rep_row = mr.aggregate_rows(feat_contrib_mat,
                                                                              n_feats_shown,
                                                                              agg_method='abs_max')
    xlabel_names = [None] * n_labels
    for i, col in enumerate(mr.order_col_):
        xlabel_names[i] = emotion_names[unique_labels[col]]

    ylabel_names = np.array(feature_names, dtype=object)[label_to_rep_row]
    for i in range(len(ylabel_names)):
        name = ylabel_names[i]
        rows = label_to_rows[i]
        if len(rows) > 1:
            ylabel_names[i] = name + ', ' + str(len(rows) - 1) + ' more'
    """

    #emotion_names = [emotion_names[i] for i in unique_labels]
    print(feat_contrib_mat.shape, len(emotion_names), len(feature_names))
    print(type(feat_contrib_mat), type(emotion_names), type(feature_names))
    return simplify(feat_contrib_mat, emotion_names, feature_names)

    #return np.asmatrix(feat_contrib_mat).tolist(), emotion_names, feature_names
    #return agg_feat_contrib_mat, xlabel_names, ylabel_names

