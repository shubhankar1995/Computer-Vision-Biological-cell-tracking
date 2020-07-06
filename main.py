import sys

from directory_reader import DirectoryReader
from preprocessor import Preprocessor

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

