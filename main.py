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
    directory_reader = DirectoryReader(sys.argv[1])
    filepaths = directory_reader.get_filepaths()

    # Test
    image = cv.imread(filepaths[0], cv.IMREAD_GRAYSCALE)
    thresholder = Thresholder(image)
    thresholded_image = thresholder.threshold()
    cv.imwrite(thresholded_image)

