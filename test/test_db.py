import unittest
from db.utils import get_connection_and_cursor, insert, select
from art.artwork import Artwork, Association


class MyTestCase(unittest.TestCase):
    def test_connection(self):
        con, cur = get_connection_and_cursor()
        self.assertIsNotNone(con)
        self.assertIsNotNone(cur)

    def test_insert(self):
        artwork = Artwork(None, "Lorem Ipsum lorem ipsum", None, None, 0)
        associations = [Association([0, 0, 10, 20], [0, 5]),
                        Association([2, 4, 5, 8], [6, 9])]

        try:
            insert(artwork, associations)
        except:
            self.fail()

    def test_selection(self):
        art = Artwork("test", "desc", "url", 1000, 0)
        ground_truth = [Association([0, 0, 10, 20], [0, 5]),
                        Association([2, 4, 5, 8], [6, 9])]

        associations = select(art)
        if len(ground_truth) != len(associations):
            self.fail()


if __name__ == '__main__':
    unittest.main()
