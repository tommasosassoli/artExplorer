from abc import ABC, abstractmethod
from art.segment.description import DotSegmentizer, CommaSegmentizer
from art.segment.image import BingSegmentizer, FastRcnnSegmentizer, SamSegmentizer


class Segmentizer(ABC):
    @abstractmethod
    def elaborate(self, ):
        pass


class ImageSegmentizer(Segmentizer):
    def __init__(self, artwork_image):
        self.artworkImage = artwork_image

    def elaborate(self):
        flat_img = self.artworkImage.get_image()

        bing = BingSegmentizer(flat_img)
        frcnn = FastRcnnSegmentizer(flat_img)

        self.artworkImage.add_segment(bing.make_segments())
        self.artworkImage.add_segment(frcnn.make_segments())

    def elaborate_coordinates(self, x, y):
        flat_img = self.artworkImage.get_image()

        sam = SamSegmentizer(flat_img)
        self.artworkImage.add_segment(sam.make_segments())


class DescriptionSegmentizer(Segmentizer):
    def __init__(self, artwork_description):
        self.artworkDescription = artwork_description

    def elaborate(self):
        flat_desc = self.artworkDescription.get_description()
        dot = DotSegmentizer(flat_desc)
        self.artworkDescription.add_segment(dot.make_segments())

