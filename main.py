import cv2 as cv
import sys

from directory_reader import DirectoryReader
import matplotlib.pyplot as plt 
from preprocessor import Preprocessor
from segment_finder import SegmentFinder
from watershed import Watershed

if __name__ == '__main__':
    # Check argv
    if len(sys.argv) < 2:
        sys.exit(
            'Please provide the path to images sequence directory.\n'\
            f'Example: python3 {sys.argv[0]} path/to/images'
        )

    # Get filepaths
    filepaths = DirectoryReader(sys.argv[1]).get_filepaths()

    # Preprocessing Test - Please delete these with the real project code
    image = cv.imread(filepaths[0], cv.IMREAD_GRAYSCALE)
    preprocessed_image = Preprocessor(image).preprocess()
    # Test - end

    # Watershed Test - Please delete these with the real project code
    watershedder = Watershed(preprocessed_image)
    result = watershedder.perform()
    print(result.max())
    plt.imshow(result)
    plt.savefig('results/watershed.png')
    # Test - end

    # Segment Finder Test - Please delete these with the real project code
    segments = SegmentFinder(result).find()
    for segment in segments:
        print(segment)
    # Test - end

    



