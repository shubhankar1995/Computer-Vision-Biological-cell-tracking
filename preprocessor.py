import cv2 as cv
import numpy as np
import sys
import time

from contrast_stretcher import ContrastStretcher
from min_max_filter import MinMaxFilter
from otsu_thresholder import OtsuThresholder
from thresholder import Thresholder
from skimage.filters import frangi

import random as rng


class Preprocessor:
    FLUO_THRESHOLD = 129
    DIC_THRESHOLD = 5

    def __init__(self, image, mode):
        self.image = image
        self.mode = mode

    def preprocess(self):
        image = self.image
        kernel = np.ones((5, 5), np.uint8)
        if self.mode == 0:  # DIC
            image = frangi(image, sigmas=[15])
            image = ContrastStretcher(image).stretch()
            image = Thresholder(image, Preprocessor.DIC_THRESHOLD).threshold()
        if self.mode == 1:  # Fluo:
            image = Thresholder(image, Preprocessor.FLUO_THRESHOLD).threshold()
        else:       # PhC
            image = MinMaxFilter(image).filter()
            image = OtsuThresholder(image).threshold()

        # Morphology
        image = cv.morphologyEx(image, cv.MORPH_OPEN, kernel)
        image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
        return image


# Used for experiments
if __name__ == '__main__':
    image = cv.imread(sys.argv[1], cv.IMREAD_GRAYSCALE)
    # cv.imwrite('results/original.png', image)          # TODO: remove

    kernel = np.ones((5, 5), np.uint8)
    mode = sys.argv[2]
    if mode == 1:    # Fluo
        image = Thresholder(image, 129).threshold()
        cv.imwrite('results/thresholded.png', image)
        image = cv.morphologyEx(image, cv.MORPH_OPEN, kernel)
        image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
        cv.imwrite('results/morphed.png', image)
    elif mode == 2:                   # PhC
        image = ContrastStretcher(image).stretch()
        cv.imwrite('results/stretched.png', image)
        # image = cv.medianBlur(image, 5)
        # cv.imwrite('results/blurred.png', image)
        # image = cv.fastNlMeansDenoising(image)
        # cv.imwrite('results/denoised.png', image)
        image = MinMaxFilter(image).filter()
        cv.imwrite('results/filtered.png', image)
        # image = ContrastStretcher(image).stretch()
        # cv.imwrite('results/post-stretched.png', image)
        image = OtsuThresholder(image).threshold()
        cv.imwrite('results/thresholded.png', image)
        image = cv.morphologyEx(image, cv.MORPH_OPEN, kernel)
        image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
        cv.imwrite('results/morphed.png', image)
    else:
        # image = ContrastStretcher(image).stretch()
        # image = cv.medianBlur(image, 5)
        # cv.imwrite('results/blurred.png', image)
        # image = cv.fastNlMeansDenoising(image)
        # cv.imwrite('results/denoised.png', image)

        image = frangi(image, sigmas=[15])
        cv.imwrite('results/frangi.png', image)

        image = ContrastStretcher(image).stretch()
        cv.imwrite('results/stretched.png', image)

        image = Thresholder(image, 5).threshold()
        cv.imwrite('results/thresholded.png', image)

        image = cv.morphologyEx(image, cv.MORPH_OPEN, kernel, iterations=2)
        cv.imwrite('results/morph_opened.png', image)
        image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
        cv.imwrite('results/morph_closed.png', image)

        threshold = 100
        canny_output = cv.Canny(image, threshold, threshold * 2)

        # Find Contour
        _, contours, _ = cv.findContours(
            canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )

        drawing = np.zeros(
            (canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

        ellipses = list()
        for i, contour in enumerate(contours):
            color = (rng.randint(0, 256), rng.randint(
                0, 256), rng.randint(0, 256))
            cv.drawContours(drawing, contours, i, color)
            if contour.shape[0] > 5:
                ellipse = cv.fitEllipse(contour)
                ellipses.append(ellipse)
                cv.ellipse(drawing, ellipse, color, 2)

        cv.imwrite('results/ellipse.png', drawing)

        # image = cv.Canny(image, 100, 200)
        # cv.imwrite('results/edges.png', image)

        # circles = cv.HoughCircles(
        #     image, cv.HOUGH_GRADIENT, 1, 20, param1=50, param2=30,
        #     minRadius=0, maxRadius=0
        # )
        # cimage = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
        # circles = np.uint16(np.around(circles))
        # for idx, i in enumerate(circles[0, :]):
        # cv.circle(cimage, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # cv.imwrite(f"results/circle.png",
        #            cimage)

        # image, contours, hierarchy = cv.findContours(
        #     image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        # )
        # cimage = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
        # cimage = cv.drawContours(cimage, contours, -1, (0, 255, 0), 3)
        # cv.imwrite('results/contour.png', cimage)
