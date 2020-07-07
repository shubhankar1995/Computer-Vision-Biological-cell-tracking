import numpy as np
import cv2 as cv

class ContrastStretcher:
    def __init__(self, image, min_clip=0, max_clip=255):
        self.image = image
        self.min_clip = min_clip
        self.max_clip = max_clip
    
    def stretch(self):
        self.clip()
        min, max = self.image.min(), self.image.max()
        return ((self.image - min) / (max - min) * 255).astype(np.uint8)

    def clip(self):
        for (r, c), pixel in np.ndenumerate(self.image):
            self.image[r, c] = min(max(pixel, self.min_clip), self.max_clip)
            