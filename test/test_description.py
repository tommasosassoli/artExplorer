from unittest import TestCase
from art.segmentizer import CommaSegmentizer


class Test(TestCase):
    def test_description_segment_encoding(self):
        text = "His hair caught in a wind, the wanderer gazes out on a landscape covered in a thick sea of fog."
        comma = CommaSegmentizer(text)
        seg = comma.make_segments()

        ground_truth = [[0, 25], [26, 95]]
        for i in range(len(ground_truth)):
            if seg[i].start_end_pos != ground_truth[i]:
                self.fail()
