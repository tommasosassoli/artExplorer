from abc import ABC, abstractmethod
from art.segment.description import DotSegmentizer
from art.segment.image import FullImageSegmentizer


class Segmentizer(ABC):
    @abstractmethod
    def elaborate(self, ):
        pass


class ImageSegmentizer(Segmentizer):
    def __init__(self, artwork_image):
        self.artworkImage = artwork_image

    def elaborate(self):
        flat_img = self.artworkImage.get_image()
        full = FullImageSegmentizer(flat_img)
        self.artworkImage.add_segment(full.make_segments())

    def elaborate_coordinates(self, x, y):
        # flat_img = self.artworkImage.get_image()
        #
        # sam = SamSegmentizer(flat_img)
        # self.artworkImage.add_segment(sam.make_segments())
        pass


class DescriptionSegmentizer(Segmentizer):
    def __init__(self, artwork_description):
        self.artworkDescription = artwork_description

    def elaborate(self):
        flat_desc = self.artworkDescription.get_description()
        dot = DotSegmentizer(flat_desc)
        self.artworkDescription.add_segment(dot.make_segments())

