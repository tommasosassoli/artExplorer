import logging
logging.basicConfig(filename='log/batch.log',
                    level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s:%(processName)s::%(message)s')

import gc
from art.analysis import Analyzer
from art.data import get_artwork_list
from db.utils import select, insert
from tqdm import tqdm


def batch():
    artwork_list = get_artwork_list()
    logging.info('Start batch process')
    for art in tqdm(artwork_list):
        segments = select(art)
        if segments is None:
            try:
                # make the analysis and insert into db
                logging.info('Analyzing ' + art.get_title() + ' (id:' + str(art.get_artpedia_id()) + ')')
                analyzer = Analyzer(art)
                segments = analyzer.analyze()
                insert(art, segments)
            except Exception as exc:
                logging.error('Exception: ' + str(exc))
            finally:
                del analyzer
                gc.collect()
    logging.info('End batch process')


if __name__ == "__main__":
    batch()
