import server.loaders.DeapLoader as DeapLoader

loader = {
    'deap': DeapLoader.convert_dataset,
    'deap_ch': DeapLoader.load_signals
}


def load_signals(dataset, conf):
    if dataset in loader.keys():
        return loader[dataset + '_ch'](conf.get('dataset', dataset + '_folder'))
    return []


def convert_dataset(dataset, dataset_folder, out_folder):
    if dataset not in loader.keys():
        return
    loader[dataset](dataset_folder, out_folder)
