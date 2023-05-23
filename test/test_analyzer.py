from unittest import TestCase
from art.data import DataFacade
from art.analyzer import ArtworkAnalyzer
from PIL import ImageDraw


def show_analysis(img, bboxes):
    draw = ImageDraw.Draw(img)
    for box in bboxes:
        draw.rectangle(box, outline=(255, 0, 0), width=2)
    img.show()


class TestArtworkAnalyzer(TestCase):
    def test_analyze(self):
        data = DataFacade()
        artwork = data.get_artwork({'title': 'Wanderer above the Sea of Fog'})

        analyzer = ArtworkAnalyzer(artwork)
        analysis = analyzer.analyze()

        pil_img = artwork.get_artwork_image().get_image().copy()
        bboxes = [a[0] for a in analysis]
        show_analysis(pil_img, bboxes)
