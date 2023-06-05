class Artwork:
    """
        Artwork class contains the image and the description
        of an artwork

        Attributes
        ----------
        title : the title of the artwork
        description : the complete description of the artwork
        url : the url to the image of the artwork
    """

    def __init__(self, title: str, description: str, url: str):
        self.title = title
        self.description = description
        self.url = url

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def set_description(self, description: str):
        if description is not None:
            self.description = description

    def get_url(self):
        return self.url


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


from art.data import PILReader, GPTApi
from art.models.vlm import GradCAM, CLIPDistance
from art.models.vm import SAM, FasterRCNN


class Analyzer:
    """
        Analyzer class is useful for make the analysis of the Artwork.

        Attributes
        ----------
        artwork : is the artwork to analyze

        Methods
        -------
        analyze() : produce all the possible association between bbox and tbox

    """

    def __init__(self, artwork: Artwork):
        self.artwork = artwork

    def analyze(self) -> list[Association] or int:
        """
        Make the analysis of an artwork
        :return: list of Association object between bbox and tbox
        """
        if self.artwork is None:
            return 404

        title = self.artwork.get_title()
        url = self.artwork.get_url()
        desc = self.artwork.get_description()

        # looking artwork task
        pil_reader = PILReader(url)
        gpt_reader = GPTApi(title, desc)

        pil_image = pil_reader.read()
        desc = gpt_reader.send()

        self.artwork.set_description(desc)  # TODO check if artwork to be return

        # analyze artwork task
        sam = SAM(pil_image)
        faster = FasterRCNN(pil_image)

        sentences = desc.split('.')

        grad = GradCAM(sam, pil_image, sentences)
        clip = CLIPDistance(faster, sentences)

        assoc = []
        assoc += grad.eval()
        assoc += clip.eval()

        return assoc
