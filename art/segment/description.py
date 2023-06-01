from abc import ABC, abstractmethod
from ..model import DescriptionSegment


class AbstractDescriptionSegmentizer(ABC):
    def __init__(self, description):
        self.description = description

    @abstractmethod
    def make_segments(self):
        pass


class DotSegmentizer(AbstractDescriptionSegmentizer):
    def make_segments(self):
        # text heuristic
        descriptions = self.description.split('.')

        # calc of start end position for descriptions
        positions = []
        start = 0
        for d in descriptions:
            end = start + len(d)
            positions.append([start, end])
            start = end + 1

        # creation of DescriptionSegments
        description_segments = []
        for i in range(len(descriptions)):
            desc_encoded = DescriptionSegment(descriptions[i], positions[i])
            description_segments.append(desc_encoded)
        return description_segments
