from abc import ABC, abstractmethod
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
from .model import Artwork, ArtworkImage, ArtworkDescription


class DataFacade:
    def __init__(self, dataset_folder=None):
        if dataset_folder is None:
            dataset_folder = '../dataset/'
        self.artpedia_dataset = ArtpediaReader(dataset_folder + 'artpedia.json')

    def get_artwork(self, params):
        return self.artpedia_dataset.get_artwork(params)


class DatasetReader(ABC):
    @abstractmethod
    def get_artwork(self, params):
        pass


class ArtpediaReader(DatasetReader):
    def __init__(self, path):
        self.path = path
        self.df = pd.read_json(self.path, orient='index')

    def get_artwork(self, params):
        title = params['title']
        obj = self.df.loc[self.df['title'] == title]
        if not obj.empty:
            # visual_sentences
            sentences = obj['visual_sentences']
            sentences = sentences.iloc[0]
            artwork_description = ArtworkDescription(' '.join(sentences))

            # image
            url = obj['img_url']
            url = url.iloc[0]
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15'}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                artwork_image = ArtworkImage(img, url)

                # build Artwork object
                return Artwork(artwork_image, artwork_description)
        return None
