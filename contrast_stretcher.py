import numpy as np
import cv2 as cv


class ContrastStretcher:
    def __init__(self, image):
        self.image = image

    def stretch(self):
        min, max = self.image.min(), self.image.max()
        return ((self.image - min) / (max - min) * 255).astype(np.uint8)
