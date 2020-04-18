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
    return send_file("./assets/index.html")


@app.route('/media/<regex("[0-9]+"):mId>/stream/')
@app.route('/media/<regex("[0-9]+"):mId>/stream/<regex("index[0-9]+.ts"):segname>/')
def hls_stream_handler(mId, segname=None):
    if not segname:
        file = f"./assets/media/{mId}/hls/index.m3u8"
        response = make_response(send_file(file))
        response.headers["Content-Type"] = "application/x-mpegURL"
    else:
        file = f"./assets/media/{mId}/hls/{segname}"
        response = make_response(send_file(file))
        response.headers["Content-Type"] = "video/MP2T"
    return response


if __name__ == "__main__":
    app.run()
