import cv2 as cv
import sys

from boxes_drawer import BoxesDrawer
from directory_reader import DirectoryReader
from preprocessor import Preprocessor
from segment_finder import SegmentFinder
from watershed import Watershed


class Processor:
    def __init__(self, file):
        self.file = file

    def process(self):
        # Read image
        image = cv.imread(self.file, cv.IMREAD_GRAYSCALE)

        # Preprocess image
        preprocessed_image = Preprocessor(image).preprocess()

        # Segment image
        segmented_image = Watershed(preprocessed_image).perform()

        # Find segments
        segments = SegmentFinder(segmented_image).find()

        # Draw bounding box
        return BoxesDrawer(segments, image).draw()


if __name__ == '__main__':
    # Check argv
    if len(sys.argv) < 2:
        sys.exit(
            'Please provide the path to images sequence directory.\n'
            f'Example: python3 {sys.argv[0]} path/to/images'
        )

    # Get files
    sequence_files = DirectoryReader(sys.argv[1]).get_sequence_files()
    if len(sequence_files) == 0:
        sys.exit(f"There are no files in '{sys.argv[1]}'.")

    # Run
    print(f'There are {len(sequence_files)} images.')
    for i, file in enumerate(sequence_files):
        print(f'Processing file {i}...')
        image = Processor(file).process()
        cv.imwrite(f'result_sequence/{i:04d}.png', image)
        print(f'File {i} done!')
