from flask import Flask, render_template, abort, jsonify
from definitions import CONFIG_PATH
import configparser
from art.analysis import Analyzer
from art.data import lookup_artwork, get_artwork_list
from db.utils import select, insert

# flask
app = Flask(__name__)

# config
config = configparser.ConfigParser()
config.read(CONFIG_PATH)


@app.route("/")
def index():
    max_artworks = int(config['web']['max_artwork_homepage'])
    artworks = get_artwork_list()
    artworks = artworks[0:max_artworks]
    return render_template('index.html', artworks=artworks)


@app.route("/<title>")
def analysis(title):
    return render_template('analysis.html', title=title)


@app.route("/api/analysis/<title>")
def api_analysis(title):
    artwork = lookup_artwork(title)
    if artwork is not None:
        # check if artwork is in database
        segments = select(artwork)

        if segments is None:
            # make analysis and store the result
            analyzer = Analyzer(artwork)
            segments = analyzer.analyze()
            insert(artwork, segments)

        # parsing segments
        seg_parse = parse_segments(segments)
        url = artwork.get_url()
        desc = artwork.get_description()

        results = {'img_url': url,
                   'desc': desc,
                   'segments': seg_parse}
        return jsonify(results)
    else:
        return abort(500)


@app.route("/api/search/<title>")
def api_search(title):
    artworks = get_artwork_list(title)
    j = [{'title': a.title,
          'img_url': a.url,
          'year': a.year
          }
         for a in artworks]

    return jsonify(j)


@app.route("/api/page/<page>")
def api_page(page):
    page = int(page)
    max_artworks = int(config['web']['max_artwork_homepage'])
    start = max_artworks * page
    end = start + max_artworks

    artworks = get_artwork_list()
    try:
        artworks = artworks[start:end]

        j = [{'title': a.title,
              'img_url': a.url,
              'year': a.year
              }
             for a in artworks]
        return jsonify(j)
    except:
        abort(404)


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
