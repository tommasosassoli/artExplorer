from torch import stack


class Artwork:
    def __init__(self, artwork_image, artwork_description):
        self.image = artwork_image
        self.description = artwork_description

    def get_artwork_image(self):
        return self.image

    def get_artwork_description(self):
        return self.description

    def has_segment(self):
        return self.image.has_segment() and self.description.has_segment()


class ArtworkDescription:
    def __init__(self, description):
        self.description = description
        self.segments = []

    def add_segment(self, segment):
        self.segments += segment

    def has_segment(self):
        return len(self.segments) > 0

    def get_segment_encoded(self):
        return stack([s.description_encoded for s in self.segments])

    def get_description(self):
        return self.description


class ArtworkImage:
    def __init__(self, image, url=None):
        self.image = image
        self.url = url
        self.segments = []

    def add_segment(self, segment):
        self.segments += segment

    def has_segment(self):
        return len(self.segments) > 0

    def get_segment_encoded(self):
        return stack([s.image_encoded for s in self.segments])

    def get_image(self):
        return self.image

    def get_url(self):
        return self.url


class DescriptionSegment:
    def __init__(self, description_encoded, start_end_pos=None):
        self.description_encoded = description_encoded
        self.start_end_pos = start_end_pos


class ImageSegment:
    def __init__(self, image_encoded, bbox=None):
        self.image_encoded = image_encoded
        self.bbox = bbox