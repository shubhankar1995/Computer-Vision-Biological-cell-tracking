import cv2 as cv
import numpy as np
from copy import deepcopy

from contrast_stretcher import ContrastStretcher
from min_max_filter import MinMaxFilter
from thresholder import Thresholder
from dilationErosion import DilationErosion

class Preprocessor:
    def __init__(self, image):
        self.image = image

    def normalizeImage(self, img, h, w):
        minVal = img.min()
        maxVal = img.max()
        Image_O = deepcopy(img)
        for i in range(h):
            for j in range(w):
                Image_O[i][j] = 255*((img[i][j] - minVal )/( maxVal - minVal))
        return Image_O

    def preprocess(self):
        image = self.image
        cv.imwrite('results/1_original.png', image)          # TODO: remove
        image = ContrastStretcher(image).stretch()
        cv.imwrite('results/2_stretched.png', image)                # TODO: remove
        image = cv.medianBlur(image, 5)
        cv.imwrite('results/3_blurred.png', image)              # TODO: remove
        # image = cv.medianBlur(image, 5)
        # cv.imwrite('results/3_2_blurred.png', image)              # TODO: remove
        image = cv.fastNlMeansDenoising(image)
        cv.imwrite('results/4_denoised.png', image)                # TODO: remove
        
        # image4 = DilationErosion(image).getBorder()
        # cv.imwrite('results/9_border.png', image4) 
        
        
        image5 = MinMaxFilter(image).filter()        
        cv.imwrite('results/5_filtered.png', image)               # TODO: remove
        image6 = ContrastStretcher(image5).stretch() 
        cv.imwrite('results/6_post-stretched.png', image)     # TODO: remove
        
        
        
        image = Thresholder(image6).threshold() 
        cv.imwrite('results/7_thresholded.png', image)            # TODO: remove
        # image2 = DilationErosion(image).getDilateErode() 
        # cv.imwrite('results/8_DilateErode.png', image2)            # TODO: remove
        # image3 = DilationErosion(image).getErodeDilate() 
        # cv.imwrite('results/9_ErodeDilate.png', image3)            # TODO: remove

        image8 = np.absolute(image5.astype('int') - image6.astype('int'))
        cv.imwrite("results/8_1_thresholded.png", image8)

        (h, w) = image8.shape
        image10 = self.normalizeImage(image8, h, w)
        cv.imwrite('results/8_3_normalized.png', image10) 

        image9 = Thresholder(image10).threshold() 
        cv.imwrite('results/8_2thresholded.png', image9) 
        


        return image