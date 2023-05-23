from .segmentizer import ImageSegmentizer, DescriptionSegmentizer
import torch


class ArtworkAnalyzer:
    def __init__(self, artwork):
        self.artwork = artwork

    def elaborate_segment(self):
        # elaborate segment
        image_seg = ImageSegmentizer(self.artwork.get_artwork_image())
        desc_seg = DescriptionSegmentizer(self.artwork.get_artwork_description())
        image_seg.elaborate()
        desc_seg.elaborate()

    def analyze(self, ):
        if not self.artwork.has_segment():
            self.elaborate_segment()

        with torch.no_grad():
            image_segments = self.artwork.get_artwork_image()
            image_segments_encoded = image_segments.get_segment_encoded()

            description_segments = self.artwork.get_artwork_description()
            description_segments_encoded = description_segments.get_segment_encoded()

            assoc = []
            for img_index, image_seg in enumerate(image_segments_encoded):
                dist = (100.0 * image_seg @ description_segments_encoded.T)
                probs = dist.softmax(dim=-1).cpu().topk(1, dim=-1)

                desc_index = probs.indices.numpy()[0][0]  # index of the most probably description
                bbox = image_segments.segments[img_index].bbox.tolist()
                start_end_pos = description_segments.segments[desc_index].start_end_pos

                assoc.append((bbox, start_end_pos))
            return assoc

    def analyze_coordinates(self, x, y):
        # TODO elaborate segment, then CLIP
        image_seg = ImageSegmentizer(self.artwork.get_artwork_image())
        image_seg.elaborate_coordinates(x, y)
