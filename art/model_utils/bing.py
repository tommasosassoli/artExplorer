import cv2.saliency as sy


bing = sy.ObjectnessBING_create()
bing.setTrainingPath("/Users/tommaso/DataspellProjects/test-tesi/opencv/models")