import cv2 as cv
import global_vars
import sys
import numpy as np

from cell_snapshot import CellSnapshot
from contrast_stretcher import ContrastStretcher
from min_max_filter import MinMaxFilter
from otsu_thresholder import OtsuThresholder
from thresholder import Thresholder


class EllipseFitter:
    CANNY_THRESHOLD = 100
    MIN_CONTOUR_POINTS = 5

    def __init__(self, image, mode):
        self.image = image
        self.mode = mode

    def fit(self):
        # Canny
        threshold = EllipseFitter.CANNY_THRESHOLD
        edges = cv.Canny(self.image, threshold, threshold * 2)

        # Find Contour
        _, contours, _ = cv.findContours(
            edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )

        ellipses = list()
        for i, contour in enumerate(contours):
            if contour.shape[0] > EllipseFitter.MIN_CONTOUR_POINTS:
                ellipse = cv.fitEllipse(contour)
                if self.is_size_ok(ellipse):
                    ellipses.append(ellipse)

        return np.array([CellSnapshot(*ellipse) for ellipse in ellipses])

    def is_size_ok(self, ellipse):
        if self.mode != 0:
            return True

        width, height = ellipse[1]
        ratio = (width * height) / global_vars.image_area
        return 0.01 < ratio and ratio < 0.2

        # Used for experiments
if __name__ == '__main__':
    image = cv.imread(sys.argv[1], cv.IMREAD_GRAYSCALE)
    cv.imwrite('results/original.png', image)          # TODO: remove

    kernel = np.ones((5, 5), np.uint8)
    mode = int(sys.argv[2])
    if mode == 1:    # Fluo
        image = Thresholder(image, 129).threshold()
        image = cv.morphologyEx(image, cv.MORPH_OPEN, kernel)
        image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
    else:                   # PhC
        image = ContrastStretcher(image).stretch()
        cv.imwrite('results/stretched.png', image)
        image = MinMaxFilter(image).filter()
        image = OtsuThresholder(image).threshold()

    EllipseFitter(image).fit()
