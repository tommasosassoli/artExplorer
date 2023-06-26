from art.artwork import Artwork
from definitions import DATASET_PATH
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import openai
import os


def read_dataset(path):
    return pd.read_json(path, orient='index')


def lookup_artwork(title) -> Artwork or None:
    if dataframe is None:
        read_dataset(DATASET_PATH)
    obj = dataframe.loc[dataframe['title'].str.contains(title, case=False, regex=False)]

    if not obj.empty:
        title = obj['title'].iloc[0]
        url = obj['img_url'].iloc[0]
        year = obj['year'].iloc[0]
        sentences = obj['visual_sentences'].iloc[0]
        desc = '\n'.join(sentences)
        index = int(obj.index[0])
        return Artwork(title, desc, url, year, index)
    return None


def get_artwork_list(title=None) -> list[Artwork]:
    if dataframe is None:
        read_dataset(DATASET_PATH)

    df = dataframe
    if title is not None:
        df = dataframe.loc[dataframe['title'].str.contains(title, case=False, regex=False)]

    list_artwork = []
    for index, row in df.iterrows():
        title = row['title']
        url = row['img_url']
        year = row['year']
        sentences = row['visual_sentences']
        desc = '\n'.join(sentences)
        list_artwork.append(Artwork(title, desc, url, year, index))

    return list_artwork


class PILReader:
    """
    PILReader is the class that read the image from an url.
    """

    def __init__(self, url: str):
        """
        :param url: is the url where download the image
        """
        self.url = url

    def read(self) -> Image:
        """
        :return: a PILImage (Pillow Image)
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15'}
        response = requests.get(self.url, headers=headers)

        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        return None


class GPTApi:
    """
    GPTApi is the class that make a call to the Gpt api
    and return a response
    """

    def __init__(self, title: str, description: str):
        """
        :param title: is the query to send to the api
        """
        self.query = 'Describe the "' + title + '" painting, basing on the following sentences: \n' + description

    def send(self) -> str:
        """
        :return: the response from the api
        """
        openai.api_key = os.getenv('OPENAI_API_KEY')
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are an helpful assistant for visual artwork description that produce long descriptions."},
                {"role": "user", "content": self.query}
            ],
            temperature=0.3
        )
        return completion.choices[0].message.content


# read dataset on init data.py
dataframe = read_dataset(DATASET_PATH)
