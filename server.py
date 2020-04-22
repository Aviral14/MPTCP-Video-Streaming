import sys
from flask import Flask, render_template, make_response, send_file
from werkzeug.routing import BaseConverter

app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters["regex"] = RegexConverter


@app.route("/")
def index_server():
    return render_template("./assets/index.html", context={addr: addr})


@app.route('/media/<regex("[0-9]+"):mId>/stream/')
@app.route('/media/<regex("[0-9]+"):mId>/stream/<regex("index[0-9]+.ts"):segname>/')
def hls_stream_handler(mId, segname=None):
    if not segname:
        file = f"./assets/media/{mId}/hls/index.m3u8"
        response = make_response(send_file(file))
        response.headers["Content-Type"] = "application/x-mpegURL"
        response.headers["Cache-Control"] = "public, max-age=10"
    else:
        file = f"./assets/media/{mId}/hls/{segname}"
        response = make_response(send_file(file))
        response.headers["Content-Type"] = "video/MP2T"
        response.headers["Cache-Control"] = "public, max-age=10"
    return response


if __name__ == "__main__":
    if len(sys.argv) == 1:
        addr = "localhost:5000"
    else:
        addr = sys.argv[1]
    app.run(host="0.0.0.0")
