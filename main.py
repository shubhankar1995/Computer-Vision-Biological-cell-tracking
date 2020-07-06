import sys
import cv2 as cv

from contrast_stretcher import ContrastStretcher
from directory_reader import DirectoryReader
from min_max_filter import MinMaxFilter
from thresholder import Thresholder

if __name__ == '__main__':
    # Check argv
    if len(sys.argv) < 2:
        sys.exit(
            'Please provide the path to images sequence directory.\n'\
            f'Example: python3 {sys.argv[0]} path/to/images'
        )

    # Get filepaths
    filepaths = DirectoryReader(sys.argv[1]).get_filepaths()

    # Test - Please delete these with the real project code
    image = cv.imread(filepaths[0], cv.IMREAD_GRAYSCALE)
    stretched_image = ContrastStretcher(image).stretch()
    cv.imwrite('stretched.png', stretched_image)
    filtered_image = MinMaxFilter(stretched_image).filter()
    cv.imwrite('filtered.png', filtered_image)
    stretched_filtered_image = ContrastStretcher(filtered_image).stretch()
    cv.imwrite('stretched_filtered.png', stretched_filtered_image)
    thresholded_image = Thresholder(stretched_filtered_image).threshold()
    cv.imwrite('thresholded.png', thresholded_image)
    # Test - end

