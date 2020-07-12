import cv2 as cv

import numpy as np  # TODO: Remove

from contrast_stretcher import ContrastStretcher
from min_max_filter import MinMaxFilter
from thresholder import Thresholder
from watershed import Watershed


class Preprocessor:
    def __init__(self, image):
        self.image = image

    def preprocess(self):
        image = self.image
        cv.imwrite('results/original.png', image)          # TODO: remove
        image = ContrastStretcher(image).stretch()
        cv.imwrite('results/stretched.png', image)
        image = cv.medianBlur(image, 5)
        image = cv.GaussianBlur(image, (5, 5), 0)
        # cv.imwrite('results/blurred.png', image)              # TODO: remove
        image = cv.fastNlMeansDenoising(image)
        # cv.imwrite('results/denoised.png', image)                # TODO: remove
        image = MinMaxFilter(image).filter()
        # cv.imwrite('results/filtered.png', image)               # TODO: remove
        image = ContrastStretcher(image).stretch()
        cv.imwrite('results/post-stretched.png', image)     # TODO: remove
        image = Thresholder(image).threshold()
        cv.imwrite('results/thresholded.png', image)            # TODO: remove
        # image = cv.Canny(image, 100, 200)
        # cv.imwrite('results/edges.png', image)            # TODO: remove

        # circles = cv.HoughCircles(
        #     image, cv.HOUGH_GRADIENT, 1, 20, param1=50, param2=30,
        #     minRadius=0, maxRadius=0
        # )
        # cimage = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
        # circles = np.uint16(np.around(circles))
        # for idx, i in enumerate(circles[0, :10]):
        #     # draw the outer circle
        #     cv.circle(cimage, (i[0], i[1]), i[2], (0, 255, 0), 2)
        #     cv.imwrite(f"results/circle_{idx}.png",
        #                cimage)            # TODO: remove

        image, contours, hierarchy = cv.findContours(
            image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )
        cimage = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
        cimage = cv.drawContours(cimage, contours, -1, (0, 255, 0), 3)
        cv.imwrite('results/contour.png', cimage)            # TODO: remove
        return image
