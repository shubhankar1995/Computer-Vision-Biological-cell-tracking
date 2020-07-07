import cv2 as cv

from contrast_stretcher import ContrastStretcher
from min_max_filter import MinMaxFilter
from thresholder import Thresholder

class Preprocessor:
    def __init__(self, image):
        self.image = image

    def preprocess(self):
        cv.imwrite('original.png', self.image)          # TODO: remove
        image = ContrastStretcher(self.image).stretch()
        cv.imwrite('stretched.png', image)              # TODO: remove
        image = cv.medianBlur(image, 5)
        cv.imwrite('blurred.png', image)                # TODO: remove
        image = MinMaxFilter(image).filter()
        cv.imwrite('filtered.png', image)               # TODO: remove
        image = ContrastStretcher(image).stretch() 
        cv.imwrite('stretched_filtered.png', image)     # TODO: remove
        image = Thresholder(image).threshold() 
        cv.imwrite('thresholded.png', image)            # TODO: remove
        return image