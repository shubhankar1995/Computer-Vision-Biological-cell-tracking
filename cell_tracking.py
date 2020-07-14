import cv2 as cv
from collections import defaultdict
import sys 
from directory_reader import DirectoryReader
from watershed import Watershed
from segment_finder import SegmentFinder

class CellTracking():
    def __init__(self):
        self.master_cell_dict = defaultdict(list)
    
    def trackCell(self, image):
        segments = SegmentFinder(image).find()
        print(segments)

    def run(self, image):
        pass




if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(
            'Please provide the path to images sequence directory.\n'
            f'Example: python3 {sys.argv[0]} path/to/images'
        )

    # Get files
    sequence_files = DirectoryReader(sys.argv[1]).get_sequence_files()
    if len(sequence_files) == 0:
        sys.exit(f"There are no files in '{sys.argv[1]}'.")

    cellTracking = CellTracking()

    # Run
    print(f'There are {len(sequence_files)} images.')
    for i, file in enumerate(sequence_files):
        if i < 1:                               #TODO: Remove
            print(f'Processing file {i}...')
            print(file)
            image = cv.imread(file, cv.IMREAD_GRAYSCALE)
            image = Watershed(image).perform()
            cellTracking.trackCell(image)
            print(f'File {i} done!')
    