from unittest import TestCase
from art.analysis import Analyzer
from art.data import PILReader, lookup_artwork
from PIL import ImageDraw


def show_analysis(img, bboxes):
    draw = ImageDraw.Draw(img)
    for box in bboxes:
        draw.rectangle(box, outline=(255, 0, 0), width=2)
    img.show()


class TestArtworkAnalyzer(TestCase):
    def test_analyze(self):
        art = lookup_artwork('Wanderer above the Sea of Fog')
        analyzer = Analyzer(art)
        analysis = analyzer.analyze()

        pil_img = PILReader(art.get_url()).read()
        bboxes = [a.bbox for a in analysis]
        show_analysis(pil_img, bboxes)
