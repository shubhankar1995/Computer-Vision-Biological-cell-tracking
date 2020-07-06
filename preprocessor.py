import cv2 as cv

from contrast_stretcher import ContrastStretcher
from min_max_filter import MinMaxFilter
from thresholder import Thresholder

class Preprocessor:
    def __init__(image):
        self.image = image

    def preprocess(self):
        stretched_image = ContrastStretcher(image).stretch()
        cv.imwrite('stretched.png', stretched_image)    # TODO: remove
        filtered_image = MinMaxFilter(stretched_image).filter()
        cv.imwrite('filtered.png', filtered_image)      # TODO: remove
        stretched_filtered_image = ContrastStretcher(filtered_image).stretch() 
        cv.imwrite('stretched_filtered.png', stretched_filtered_image)          # TODO: remove
        thresholded_image = Thresholder(stretched_filtered_image).threshold() 
        cv.imwrite('thresholded.png', thresholded_image)                        # TODO: remove
        return thresholded_image