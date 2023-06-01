from segment_anything import sam_model_registry, SamPredictor
import numpy as np


sam_checkpoint = "/Users/tommaso/DataspellProjects/test-tesi/segment-anything/sam_vit_h_4b8939.pth"
model_type = "vit_h"

device = "cpu"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
predictor = SamPredictor(sam)


def get_bbox_from_mask(mask):
    indexes = np.argwhere(mask == True)

    x = indexes[:, 1]
    y = indexes[:, 0]

    min_x = np.min(x)
    max_x = np.max(x)

    min_y = np.min(y)
    max_y = np.max(y)

    return [min_x, min_y, max_x, max_y]
