from .segmentizer import ImageSegmentizer, DescriptionSegmentizer
from .model_utils.clip import model, preprocess, tokenizer, device
from .model_utils.grad_cam import resize_image, gradCAM, get_hot_coord
from .model_utils.sam import predictor as sam_predictor, get_bbox_from_mask
import torch
import numpy as np
import cv2


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

        pil_image = self.artwork.get_artwork_image().get_image()
        description_segments = self.artwork.get_artwork_description().segments
        assoc = []

        # GradCAM
        input_image = preprocess(pil_image).unsqueeze(0).to(device)
        image_np = resize_image(pil_image, 224)

        # Segment Anything
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        sam_predictor.set_image(cv_image)

        for desc_index, caption in enumerate(description_segments):
            text_input = tokenizer([caption.description_encoded]).to(device)

            attn_map = gradCAM(
                model.visual,
                input_image,
                model.encode_text(text_input).float(),
                getattr(model.visual, "layer4")
            )
            attn_map = attn_map.squeeze().detach().cpu().numpy()
            coord = get_hot_coord(pil_image, image_np, attn_map)

            input_point = np.array([coord])
            input_label = np.array([1])

            masks, scores, logits = sam_predictor.predict(
                point_coords=input_point,
                point_labels=input_label,
                multimask_output=False,
            )

            bbox = get_bbox_from_mask(masks[0])
            bbox = np.array(bbox).tolist()      # convert all np.int64 to int Python scalar
            start_end_pos = description_segments[desc_index].start_end_pos

            assoc.append((bbox, start_end_pos))
        return assoc

    def analyze_coordinates(self, x, y):
        # TODO elaborate segment, then CLIP
        image_seg = ImageSegmentizer(self.artwork.get_artwork_image())
        image_seg.elaborate_coordinates(x, y)
