from art.analysis import Analyzer
from art.data import get_artwork_list
from db.utils import select, insert
from tqdm import tqdm


def batch():
    artwork_list = get_artwork_list()
    for art in tqdm(artwork_list):
        segments = select(art)
        if segments is None:
            # make the analysis and insert into db
            analyzer = Analyzer(art)
            segments = analyzer.analyze()
            insert(art, segments)


if __name__ == "__main__":
    batch()
