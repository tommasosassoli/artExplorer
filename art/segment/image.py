from abc import ABC, abstractmethod
from art.model import ImageSegment
import torch


class AbstractImageSegmentizer(ABC):
    def __init__(self, image):
        self.image = image

    @abstractmethod
    def make_segments(self, ):
        pass


class FullImageSegmentizer(AbstractImageSegmentizer):
    def make_segments(self, ):
        with torch.no_grad():
            seg = ImageSegment(self.image, None)
        return [seg]
