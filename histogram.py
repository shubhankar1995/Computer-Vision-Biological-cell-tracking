import cv2 as cv
import matplotlib.pyplot as plt
import sys

from contrast_stretcher import ContrastStretcher
from min_max_filter import MinMaxFilter
from thresholder import Thresholder
from watershed import Watershed

if __name__ == '__main__':
    image = cv.imread(sys.argv[1], cv.IMREAD_GRAYSCALE)
    # cv.imwrite('results/original.png', image)          # TODO: remove
    # image = ContrastStretcher(image).stretch()
    print(image.ravel())
    print(image.max())
    cv.imwrite('results/stretched.png', image)
    # image = cv.medianBlur(image, 5)
    # image = cv.GaussianBlur(image, (5, 5), 0)
    # cv.imwrite('results/blurred.png', image)
    # image = cv.fastNlMeansDenoising(image)
    # cv.imwrite('results/denoised.png', image)
    # image = MinMaxFilter(image).filter()
    # cv.imwrite('results/filtered.png', image)
    # image = ContrastStretcher(image).stretch()
    # cv.imwrite('results/post-stretched.png', image)
    plt.hist(image.ravel(), 256, [0, 256])
    plt.show()
