from abc import ABC, abstractmethod
from ..model import DescriptionSegment
from art.model_utils.clip import tokenizer, model, device


def description_segment_encoding(descriptions):
    # calc of start end position for descriptions
    positions = []
    start = 0
    for d in descriptions:
        end = start + len(d)
        positions.append([start, end])
        start = end + 1

    # CLIP encoder
    token = tokenizer(descriptions).to(device)
    features = model.encode_text(token)
    features /= features.norm(dim=-1, keepdim=True)

    # creation of DescriptionSegments
    description_segments = []
    for i in range(len(descriptions)):
        desc_encoded = DescriptionSegment(features[i], positions[i])
        description_segments.append(desc_encoded)
    return description_segments


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
        return description_segment_encoding(descriptions)
