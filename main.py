from glob import glob
from os import getcwd

import falcon
from jinja2 import Template

app = falcon.App()
dir = getcwd()


def get_files():
    files = []
    for i in ('*.png', '*.jpg', '*.jpeg'):
        files.extend(glob(f"images/{i}"))
    return sorted(files)


class HTML(object):
    def on_get(self, req, resp):
        with open("templates/index.html.j2", "r") as f:
            t = Template(f.read())
        resp.content_type = "text/html"
        resp.status = falcon.HTTP_200
        resp.text = t.render(files=get_files())


class JavaScript(object):
    def on_get(self, req, resp):
        with open("templates/carousel.js.j2") as f:
            t = Template(f.read())
        resp.content_type = "text/js"
        resp.status = falcon.HTTP_200
        resp.text = t.render(count=len(get_files()))


app.add_route("/", HTML())
app.add_route("/carousel.js", JavaScript())
app.add_static_route("/images", f"{dir}/images")
app.add_static_route("/statics", f"{dir}/statics")
