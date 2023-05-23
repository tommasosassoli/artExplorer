from abc import ABC, abstractmethod

from art.model_utils.bing import bing

from art.model_utils.clip import \
    model as clip_model, \
    device, \
    preprocess as clip_preprocess

from art.model_utils.fast_rcnn import \
    model as frcnn_model, \
    preprocess as frcnn_preprocess

from art.model import ImageSegment
from PIL import Image
import cv2
import numpy as np
import torch


def image_segment_encoding(images, bboxes):
    # CLIP transformation
    image_features = []
    with torch.no_grad():
        for img in images:
            image = clip_preprocess(img).unsqueeze(0).to(device)
            features = clip_model.encode_image(image)
            features /= features.norm(dim=-1, keepdim=True)
            image_features.append(features)

    # creation of ImageSegments
    image_segments = []
    for i in range(len(image_features)):
        segment = ImageSegment(image_features[i], bboxes[i])
        image_segments.append(segment)

    return image_segments


class AbstractImageSegmentizer(ABC):
    def __init__(self, image):
        self.image = image

    @abstractmethod
    def make_segments(self, ):
        pass


class BingSegmentizer(AbstractImageSegmentizer):
    def make_segments(self, ):
        # convert PIL image to cv2 image format
        img = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)

        # compute bing saliency
        success, map = bing.computeSaliency(img)
        max_detections = 8
        num_detections = map.shape[0]

        # make crops and bbox
        images_crop = []
        bboxes = []
        for i in range(0, min(num_detections, max_detections)):
            bbox = (startX, startY, endX, endY) = map[i].flatten()
            crop_img = img[startY:endY, startX:endX].copy()

            # transform crop_img from cv2 image to PIL image
            pil_crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
            pil_crop_img = Image.fromarray(pil_crop_img)

            bboxes.append(bbox)
            images_crop.append(pil_crop_img)
        return image_segment_encoding(images_crop, bboxes)


class FastRcnnSegmentizer(AbstractImageSegmentizer):
    def make_segments(self):
        image = frcnn_preprocess(self.image).unsqueeze(0)
        with torch.no_grad():
            prediction = frcnn_model(image)

        boxes = prediction[0]["boxes"]
        # labels = prediction[0]["labels"]
        scores = prediction[0]["scores"]
        box_num = torch.argwhere(scores > 0.6).shape[0]

        # make crops and bbox
        images_crop = []
        bboxes = []
        for i in range(box_num):
            box = (x1, y1, x2, y2) = boxes[i].numpy().astype("int")
            crop = self.image.crop(box)

            bboxes.append(box)
            images_crop.append(crop)
        return image_segment_encoding(images_crop, bboxes)


class SamSegmentizer(AbstractImageSegmentizer):
    pass