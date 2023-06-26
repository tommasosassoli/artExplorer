from art.analysis import Association
from art.models.vm import SAM, FasterRCNN
from art.models.utils.grad_cam import resize_image, gradCAM, get_hot_coord
from art.models.utils.clip import get_clip_model
from PIL import Image
import torch


def calc_tbox(descriptions: list, index: int) -> list:
    """
    Produce the tbox for a given description
    :param descriptions: list of descriptions
    :param index: index of the description to produce tbox
    :return: tbox in format [startCh, endCh]
    """
    start = 0
    for j in range(index):
        start += len(descriptions[j]) + 1
    end = len(descriptions[index]) + start
    return [start, end]


class GradCAM:
    """
    GradCAM class contains a call to GradCAM method based on CLIP
    model (https://arxiv.org/abs/1610.02391). It also contains a
    code to extract bbox using SAM, from the most red point on
    the attention-map returned by GradCAM.

    Attributes
    ----------
    descriptions : a list of description split by a heuristic (like "dot")
    """

    def __init__(self, sam: SAM, pil_image: Image, descriptions=None):
        """
        :param sam: the SAM class in vm package
        """
        self.sam = sam
        self.pil_image = pil_image
        if descriptions is None:
            descriptions = []
        self.descriptions = descriptions

        self.model, self.preprocess, self.tokenizer, self.device = get_clip_model()

    def eval(self) -> list[Association]:
        """
        :return: a list of Association object from bbox and tbox
        """
        input_image = self.preprocess(self.pil_image).unsqueeze(0).to(self.device)
        image_np = resize_image(self.pil_image, 224)

        assoc = []
        for desc_index, caption in enumerate(self.descriptions):
            text_input = self.tokenizer([caption]).to(self.device)

            attn_map = gradCAM(
                self.model.visual,
                input_image,
                self.model.encode_text(text_input).float(),
                getattr(self.model.visual, "layer4")
            )
            attn_map = attn_map.squeeze().detach().cpu().numpy()
            coord = get_hot_coord(self.pil_image, image_np, attn_map)

            # call to SAM
            bbox = self.sam.eval(coord[0], coord[1])
            tbox = calc_tbox(self.descriptions, desc_index)

            assoc.append(Association(bbox, tbox, 'GradCAM'))
        return assoc


class CLIPDistance:
    """
    CLIPDistance class contains the code to calculate the distance
    between images crop and description. It returns the most probability
    description for each image. The images are cropped by fasterRCNN
    network.

    Attributes
    ----------
    descriptions : a list of description split by a heuristic (like "dot")
    """

    def __init__(self, faster_rcnn: FasterRCNN, descriptions=None):
        """
        :param faster_rcnn: the FasterRCNN class in vm package
        """
        if descriptions is None:
            descriptions = []
        self.faster_rcnn = faster_rcnn
        self.descriptions = descriptions

        self.model, self.preprocess, self.tokenizer, self.device = get_clip_model()

    def eval(self) -> list[Association]:
        """
        :return: a list of Association object from bbox and tbox
        """
        images_crop, bboxes = self.cropping()
        assoc = []
        if len(images_crop) > 0:
            # CLIP encoding
            images_encoded = self.image_crop_encoding(images_crop)
            descriptions_encoded = self.description_encoding()

            # distance calculation
            for img_index, image_seg in enumerate(images_encoded):
                dist = (100.0 * image_seg @ descriptions_encoded.T)
                probs = dist.softmax(dim=-1).cpu().topk(1, dim=-1)

                desc_index = probs.indices.numpy()[0][0]  # index of the most probably description
                bbox = bboxes[img_index]
                tbox = calc_tbox(self.descriptions, desc_index)

                assoc.append(Association(bbox, tbox, 'CLIPDistance'))
        return assoc

    def cropping(self) -> tuple[list, list]:
        """
        Helper function
        :return: a list of crop from original image and a list
            of bbox from FasterRCNN class
        """
        bboxes = self.faster_rcnn.eval()
        pil_image = self.faster_rcnn.pil_image

        crops = []
        for bbox in bboxes:
            crops.append(pil_image.crop(bbox))
        return crops, bboxes

    def image_crop_encoding(self, images_crop: list) -> torch.tensor:
        """
        Helper function
        :param images_crop: list of crops of the image
        :return: tensor contain the crops features
        """
        # CLIP transformation
        image_features = []
        with torch.no_grad():
            for img in images_crop:
                image = self.preprocess(img).unsqueeze(0).to(self.device)
                features = self.model.encode_image(image)
                features /= features.norm(dim=-1, keepdim=True)
                image_features.append(features)
        return torch.stack(image_features)

    def description_encoding(self) -> torch.tensor:
        """
        Helper function
        :return: tensor contain the description features
        """
        # CLIP encoder
        token = self.tokenizer(self.descriptions).to(self.device)
        features = self.model.encode_text(token)
        features /= features.norm(dim=-1, keepdim=True)
        return features
