import json
from configparser import ConfigParser
import web

from server.loaders import DataLoader
from server.emoclass import EmoClassification as ec
from server.emovis import EmoDiscretization as emodis
from server.emovis import FeatureContribution as fcontrib

render = web.template.render('templates/')

urls = (
    '/', 'Index',
    '/load_signals', 'LoadSignals',
    '/process_dataset', 'ProcessDataset'
)

app = web.application(urls, globals())

# Reading file of server connection
conf = ConfigParser()
conf.read('server/server_config.cfg')

# variables
nClasses = 4
isOnline = False


class Index(object):
    def GET(self):
        return render.index()


class LoadSignals(object):
    def POST(self):
        data = json.loads(web.data())
        web.header('Content-Type', 'application/json')
        return json.dumps(DataLoader.load_signals(data["dataset"], conf))


class ProcessDataset(object):
    """
    data = {
        'dataset': idDataset,
        'fselector': id fSelector,
        'classifier': idClassifier,
        'windowSize': float,
        'windowOverlap': float,
        'signals': Array
    };
    """
    def POST(self):
        data = json.loads(web.data())
        dataset_folder = conf.get('dataset', data["dataset"] + '_folder')
        data_folder = conf.get('general', 'data_folder')
        models_folder = conf.get('general', 'models_folder')
        if isOnline:
            DataLoader.convert_dataset(data["dataset"], dataset_folder, data_folder)
        features, labels, feature_names = ec.initProcess(data, models_folder, data_folder)
        labels, emotion_names = emodis.discretize(labels, nClasses)
        featuresContrib, xlabels, ylabels = fcontrib.computeContribution(features, labels, emotion_names, feature_names)
        res = {
            'class': labels,
            'features': {'fcs': featuresContrib, 'xlabels': xlabels, 'ylabels': ylabels}
        }
        web.header('Content-Type', 'application/json')
        return json.dumps(res)


if __name__ == "__main__":
    app.run()
