import cv2 as cv
import numpy as np

class DilationErosion:
    def __init__(self, image):
        self.image = image

    def performDilation(self, img):
        kernel = np.ones((30,30), np.uint8) 
        img_dilation = cv.dilate(img, kernel, iterations=1) 
        return img_dilation

    def performErosion(self, img):
        kernel = np.ones((30,30), np.uint8) 
        img_erosion = cv.erode(img, kernel, iterations=1) 
        return img_erosion

    def getDilateErode(self):
        img_dilation = self.performDilation(self.image)
        img_erosion = self.performErosion(img_dilation)
        return img_erosion

    def getErodeDilate(self):
        img_erosion = self.performErosion(self.image)
        img_dilation = self.performDilation(img_erosion)
        return img_dilation
    
    def getBorder(self):
        img_dilation = self.performDilation(self.image)
        return img_dilation.astype('int') - self.image.astype('int')
