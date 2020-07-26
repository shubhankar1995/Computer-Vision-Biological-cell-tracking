import cv2 as cv
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

    def __init__(self, image):
        self.image = image

    def fit(self):
        # Canny
        threshold = EllipseFitter.CANNY_THRESHOLD
        canny_output = cv.Canny(self.image, threshold, threshold * 2)

        # Find Contour
        _, contours, _ = cv.findContours(
            canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )

        ellipses = list()
        for i, contour in enumerate(contours):
            if contour.shape[0] > EllipseFitter.MIN_CONTOUR_POINTS:
                ellipses.append(cv.fitEllipse(contour))

        return np.array([CellSnapshot(*ellipse) for ellipse in ellipses])


# Used for experiments
if __name__ == '__main__':
    image = cv.imread(sys.argv[1], cv.IMREAD_GRAYSCALE)
    cv.imwrite('results/original.png', image)          # TODO: remove

    kernel = np.ones((5, 5), np.uint8)
    mode = int(sys.argv[2])
    if mode == 1:    # Fluo
        image = Thresholder(image, 129).threshold()
        cv.imwrite('results/thresholded.png', image)
        image = cv.morphologyEx(image, cv.MORPH_OPEN, kernel)
        image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
        cv.imwrite('results/morphed.png', image)
    else:                   # PhC
        image = ContrastStretcher(image).stretch()
        cv.imwrite('results/stretched.png', image)
        image = MinMaxFilter(image).filter()
        image = OtsuThresholder(image).threshold()

    EllipseFitter(image).fit()
