from segment_anything import sam_model_registry, SamPredictor
from PIL import Image
from definitions import CONFIG_PATH
import configparser
import cv2
import numpy as np
import torchvision
import torch


class SAM:
    """
    Segment Anything Model: this class is an interface for
    this model by FacebookResearch (https://segment-anything.com).

    Attributes
    ----------
    predictor : SamPredictor
        is the predictor for the model
    """

    def __init__(self, pil_image: Image):
        """
        :param pil_image: PilImage
            is the image in PIL (Pillow) format
        """
        # config
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)

        sam_checkpoint = config['sam']['sam_checkpoint']
        model_type = config['sam']['model_type']
        device = config['sam']['device']

        # model init
        sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        sam.to(device=device)
        self.predictor = SamPredictor(sam)

        # image set
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        self.predictor.set_image(cv_image)

    def eval(self, x: int, y: int) -> list:
        """
        :param x: x-coordinate
        :param y: y-coordinate
        :return: a list of bbox in format [startX, startY, endX, endY]
        """
        input_point = np.array([[x, y]])
        input_label = np.array([1])

        masks, scores, logits = self.predictor.predict(
            point_coords=input_point,
            point_labels=input_label,
            multimask_output=False,
        )

        bbox = self.get_bbox_from_mask(masks[0])
        bbox = np.array(bbox).tolist()  # convert all np.int64 to int Python scalar
        return bbox

    def get_bbox_from_mask(self, mask: list):
        """
        Helper function
        :param mask: mask returned from sam predictor
        :return: bbox for the mask
        """
        indexes = np.argwhere(mask == True)

        x = indexes[:, 1]
        y = indexes[:, 0]

        min_x = np.min(x)
        max_x = np.max(x)

        min_y = np.min(y)
        max_y = np.max(y)

        return [min_x, min_y, max_x, max_y]


class FasterRCNN:
    """
    FasterRCNN: this class is an interface for
    the model based on https://arxiv.org/abs/1506.01497.
    The implementation is based on Torch.

    Attributes
    ----------
    model : model of FasterRCNN
    """

    def __init__(self, pil_image: Image):
        """
        :param pil_image: PilImage
            is the image in PIL (Pillow) format
        """
        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights='DEFAULT')
        self.model.eval()
        self.preprocess = torchvision.transforms.ToTensor()
        self.pil_image = pil_image

    def eval(self) -> list:
        """
        :return: a list of bbox in format [startX, startY, endX, endY]
        """
        image = self.preprocess(self.pil_image).unsqueeze(0)
        with torch.no_grad():
            prediction = self.model(image)

        boxes = prediction[0]["boxes"]
        scores = prediction[0]["scores"]
        box_num = torch.argwhere(scores > 0.6).shape[0]

        # make bbox list
        bboxes = []
        for i in range(box_num):
            box = boxes[i].numpy().astype("int").tolist()
            bboxes.append(box)
        return bboxes
