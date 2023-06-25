from unittest import TestCase
from art.data import lookup_artwork, GPTApi, PILReader, get_artwork_list


class TestDatasetReader(TestCase):
    def test_artpedia_exist_artwork(self):
        titles = ['Madonna of the Quail',
                  'Maestà (Cimabue)',
                  'Landscape, Branchville',
                  'Fiesole Altarpiece']

        for t in titles:
            a = lookup_artwork(t)
            if a is None:
                self.fail()

    def test_artpedia_not_exist_artwork(self):
        titles = ['abcdefg',
                  'Not Exist']

        for t in titles:
            a = lookup_artwork(t)
            if a is not None:
                self.fail()

    def test_gpt_api(self):
        title, _, desc = lookup_artwork("Wanderer above the Sea of Fog")
        api = GPTApi(title, desc)
        res = api.send()
        if res is None:
            self.fail()

    def test_pil_download(self):
        _, url, _ = lookup_artwork("Wanderer above the Sea of Fog")
        pil = PILReader(url)
        img = pil.read()
        if img is None:
            self.fail()

    def test_get_titles(self):
        t = get_artwork_list()
        if t is None or len(t) == 0:
            self.fail()
