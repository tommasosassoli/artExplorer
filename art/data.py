from abc import ABC, abstractmethod
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import openai
import os
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


def request_chat_gpt_description(title):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    query = 'Describe the "' + title + '" picture'
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are an helpful assistant for visual artwork description that produce long descriptions."},
            {"role": "user", "content": query}
        ],
        temperature=0.9
    )
    return completion.choices[0].message.content


def request_image(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    return None


class ArtpediaReader(DatasetReader):
    def __init__(self, path):
        self.path = path
        self.df = pd.read_json(self.path, orient='index')

    def get_artwork(self, params):
        title = params['title']
        obj = self.df.loc[self.df['title'].str.contains(title, case=False, regex=False)]
        if not obj.empty:
            # description with ChatGPT
            title = obj['title'].iloc[0]
            description = request_chat_gpt_description(title)
            artwork_description = ArtworkDescription(description)

            # image
            url = obj['img_url']
            url = url.iloc[0]
            img = request_image(url)

            if img is not None:
                artwork_image = ArtworkImage(img, url)

                # build Artwork object
                return Artwork(artwork_image, artwork_description)
        return None
