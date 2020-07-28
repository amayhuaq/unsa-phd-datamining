from ConfigParser import ConfigParser
import web

"""
from server.recoloring import Recoloring
from server.visenc_generator import VisualEncodingGenerator as ve
import server.reprojection.reprojection as Reprojection
"""

render = web.template.render('templates/')

urls = (
    '/', 'Index',
    '/process_image', 'ProcessImage',
    '/gen_spec', 'GenSpec',
    '/recolor', 'Recolor',
    '/reproject', 'Reproject'
)

app = web.application(urls, globals())


# Reading file of server connection
conf = ConfigParser()
conf.read('server/server_config.cfg')


"""
# MongoDB
host = conf.get('mongodb', 'host')
port = conf.getint('mongodb', 'port')
dbName = conf.get('mongodb', 'db')
client = MongoClient(host, port)
user = conf.get('mongodb', 'user')
password = conf.get('mongodb', 'password')
db = client[dbName]
images_folder = conf.get('data', 'figures_folder')
"""


class Index(object):
    def GET(self):
        return render.index()


class ProcessImage(object):
    def POST(self):
        data = json.loads(web.data())
        filename = data["filename"]
        print filename

        fig = None
        if LOAD_DB:
            fig = db.figures.find_one({'filename': filename})
            fig["fn"] = images_folder + filename
            if fig["legend"]["bbox"]["w"] > fig["legend"]["bbox"]["h"]:
                fig["legend"]["colors"].sort(key=lambda color: color["x"], reverse=False)
            else:
                fig["legend"]["colors"].sort(key=lambda color: color["y"], reverse=True)

        if fig is None:
            print "analyze image using the pipeline"

        web.header('Content-Type', 'application/json')
        return json.dumps(fig, default=json_util.default)


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


if __name__ == "__main__":
    app.run()
