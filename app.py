import json
from configparser import ConfigParser
import web

from server.loaders import DataLoader
from server.emoclass import EmoClassification as ec
from server.emovis import EmoDiscretization as emodis

render = web.template.render('templates/')

urls = (
    '/', 'Index',
    '/load_channels', 'LoadChannels',
    '/process_dataset', 'ProcessDataset',
    #'/gen_spec', 'GenSpec',
    #'/recolor', 'Recolor',
    #'/reproject', 'Reproject'
)

app = web.application(urls, globals())

# Reading file of server connection
conf = ConfigParser()
conf.read('server/server_config.cfg')


class Index(object):
    def GET(self):
        return render.index()


class LoadChannels(object):
    def POST(self):
        data = json.loads(web.data())
        web.header('Content-Type', 'application/json')
        return json.dumps(DataLoader.load_channels(data["dataset"]))


class ProcessDataset(object):
    def POST(self):
        data = json.loads(web.data())
        dataDB = DataLoader.load_dataset(data["dataset"], conf)
        #res = ec.initProcess(dataDB)
        res = {'class': emodis.discretize(dataDB['class_or'])}
        web.header('Content-Type', 'application/json')
        return json.dumps(res)

"""
class GenSpec(object):
    def POST(self):
        data = json.loads(web.data())
        myspec = ve.Spec(data)
        return json.dumps(myspec.gen(all_colors=True))


class Recolor(object):
    def POST(self):
        data = json.loads(web.data())
        fig_data = data['fig_data']
        new_colormap = data['new_colormap']

        if fig_data['legend']['type'] == 'discrete':
            new_data = Recoloring.recolor_discrete(fig_data, new_colormap)
        else:
            new_data = Recoloring.recolor_continuous(fig_data, new_colormap)

        web.header("Content-Type", "images/png")
        return new_data


class Reproject(object):
    def POST(self):
        data = json.loads(web.data())
        fig_data = data['fig_data']
        new_img = Reprojection.reproject(fig_data["filename"], fig_data["data"], fig_data["visenc"], data['new_projection'])
        web.header("Content-Type", "images/png")
        return new_img
"""

if __name__ == "__main__":
    app.run()
