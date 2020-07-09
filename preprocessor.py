import cv2 as cv

from contrast_stretcher import ContrastStretcher
from min_max_filter import MinMaxFilter
from thresholder import Thresholder
from dilationErosion import DilationErosion

class Preprocessor:
    def __init__(self, image):
        self.image = image

    def preprocess(self):
        image = self.image
        cv.imwrite('results/1_original.png', image)          # TODO: remove
        image = ContrastStretcher(image).stretch()
        cv.imwrite('results/2_stretched.png', image)                # TODO: remove
        image = cv.medianBlur(image, 5)
        cv.imwrite('results/3_blurred.png', image)              # TODO: remove
        image = cv.medianBlur(image, 5)
        cv.imwrite('results/3_2_blurred.png', image)              # TODO: remove
        image = cv.fastNlMeansDenoising(image)
        cv.imwrite('results/4_denoised.png', image)                # TODO: remove
        
        image4 = DilationErosion(image).getBorder()
        cv.imwrite('results/9_border.png', image4) 
        
        
        # image = MinMaxFilter(image).filter()        
        # cv.imwrite('results/5_filtered.png', image)               # TODO: remove
        image = ContrastStretcher(image4).stretch() 
        cv.imwrite('results/9_2_post-stretched.png', image)     # TODO: remove
        image = Thresholder(image).threshold() 
        cv.imwrite('results/9_3_thresholded.png', image)            # TODO: remove
        # image2 = DilationErosion(image).getDilateErode() 
        # cv.imwrite('results/8_DilateErode.png', image2)            # TODO: remove
        # image3 = DilationErosion(image).getErodeDilate() 
        # cv.imwrite('results/9_ErodeDilate.png', image3)            # TODO: remove
        return image