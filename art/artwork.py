class Artwork:
    """
        Artwork class contains the image and the description
        of an artwork

        Attributes
        ----------
        title : the title of the artwork
        description : the complete description of the artwork
        url : the url to the image of the artwork
        year: the year of the artwork
    """

    def __init__(self, title: str, description: str, url: str, year: int = None, artpedia_id: int = None):
        self.title = title
        self.description = description
        self.url = url
        self.year = year
        self.artpedia_id = artpedia_id

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def set_description(self, description: str):
        if description is not None:
            self.description = description

    def get_url(self):
        return self.url

    def get_year(self):
        return self.year

    def get_artpedia_id(self):
        return self.artpedia_id


class Association:
    """
        Association class represent an association between a bbox on the image
        and a tbox (text-box) on the textual description.

        Attributes
        ----------
        bbox : [startX, startY, endX, endY]
            an array representing a point on image
        tbox : [startCh, endCh]
            an array of int representing the position of substring
            over the complete description
        process : is the name of the process that generates that
            association, like GradCAM or CLIPDistance
    """

    def __init__(self, bbox: list, tbox: list, process: str = None):
        self.bbox = bbox
        self.tbox = tbox
        self.process = process
