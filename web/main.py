from flask import Flask, render_template, abort, jsonify
from art.data import DataFacade
from art.analyzer import ArtworkAnalyzer
import os

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/<title>")
def analyze_artwork(title):
    params = {'title': title}
    dataset_folder = os.getcwd() + '/dataset/'
    artwork = DataFacade(dataset_folder).get_artwork(params)

    if artwork is not None:
        analyzer = ArtworkAnalyzer(artwork)

        segments = analyzer.analyze()
        seg_parse = parse_segments(segments)
        url = artwork.get_artwork_image().get_url()
        desc = artwork.get_artwork_description().get_description()

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
                'startX': segments[i][0][0],
                'startY': segments[i][0][1],
                'endX': segments[i][0][2],
                'endY': segments[i][0][3],
            },
             'start_end_pos': {
                 'start': segments[i][1][0],
                 'end': segments[i][1][1]
             }
        }
        res.append(s)
    return res
