import cv2 as cv

from contrast_stretcher import ContrastStretcher
from min_max_filter import MinMaxFilter
from thresholder import Thresholder

class Preprocessor:
    def __init__(self, image):
        self.image = image

    def preprocess(self):
        image = self.image
        cv.imwrite('results/original.png', image)          # TODO: remove
        image = ContrastStretcher(image).stretch()
        cv.imwrite('results/stretched.png', image)                # TODO: remove
        image = cv.medianBlur(image, 5)
        cv.imwrite('results/blurred.png', image)              # TODO: remove
        image = cv.fastNlMeansDenoising(image)
        cv.imwrite('results/denoised.png', image)                # TODO: remove
        image = MinMaxFilter(image).filter()
        cv.imwrite('results/filtered.png', image)               # TODO: remove
        image = ContrastStretcher(image).stretch() 
        cv.imwrite('results/post-stretched.png', image)     # TODO: remove
        image = Thresholder(image).threshold() 
        cv.imwrite('results/thresholded.png', image)            # TODO: remove
        return image