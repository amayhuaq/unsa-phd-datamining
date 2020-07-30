import DeapLoader

loader = {
    'deap': DeapLoader.load_dataset,
    'deap_ch': DeapLoader.load_channels
}


def load_channels(dataset):
    return loader[dataset + '_ch']()


def load_dataset(dataset, conf):
    path_db = conf.get('dataset', dataset + '_folder')
    return loader[dataset](path_db)
