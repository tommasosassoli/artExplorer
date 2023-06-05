from flask import Flask, render_template, abort, jsonify
from art.analysis import Analyzer
from art.data import lookup_artwork
import os

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/<title>")
def analyze_artwork(title):
    artwork = lookup_artwork(title)
    if artwork is not None:
        analyzer = Analyzer(artwork)
        segments = analyzer.analyze()
        seg_parse = parse_segments(segments)
        url = artwork.get_url()
        desc = artwork.get_description()

        results = {'img_url': url,
                   'desc': desc,
                   'segments': seg_parse}
        return jsonify(results)
    else:
        return abort(404)


def parse_segments(segments):
    res = []
    for i in range(len(segments)):
        s = {'bbox': {
            'startX': segments[i].bbox[0],
            'startY': segments[i].bbox[1],
            'endX': segments[i].bbox[2],
            'endY': segments[i].bbox[3],
            },
            'start_end_pos': {
                'start': segments[i].tbox[0],
                'end': segments[i].tbox[1]
            },
            'process': segments[i].process
        }
        res.append(s)
    return res
