import sys
import cv2 as cv

from directoryreader import DirectoryReader
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
    thresholded_image = Thresholder(image).threshold()
    cv.imwrite('test_result.png', thresholded_image)
    # Test - end

