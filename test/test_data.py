from unittest import TestCase
from art.data import DataFacade


class TestDatasetReader(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = DataFacade()

    def test_artpedia_exist_artwork(self):
        params = [{'title': 'Madonna of the Quail'},
                  {'title': 'Maestà (Cimabue)'},
                  {'title': 'Landscape, Branchville'},
                  {'title': 'Fiesole Altarpiece'}]

        for p in params:
            a = self.data.get_artwork(p)
            if a is None:
                self.fail()

    def test_artpedia_not_exist_artwork(self):
        params = [{'title': ''},
                  {'title': ' '},
                  {'title': 'Not Exist'},
                  {'title': '.'}]

        for p in params:
            a = self.data.get_artwork(p)
            if a is not None:
                self.fail()
