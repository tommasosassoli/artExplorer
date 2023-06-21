from art.data import PILReader, GPTApi
from art.artwork import Artwork, Association
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

        self.artwork.set_description(desc)

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
