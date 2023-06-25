from flask import Flask, render_template, abort, jsonify
from art.analysis import Analyzer
from art.data import lookup_artwork, get_artwork_list

app = Flask(__name__)


@app.route("/")
def index():
    artworks = get_artwork_list()
    artworks = artworks[0:10]
    return render_template('index.html', artworks=artworks)


@app.route("/<title>")
def analysis(title):
    return render_template('analysis.html', title=title)


@app.route("/api/analysis/<title>")
def api_analysis(title):
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
        return abort(500)


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
