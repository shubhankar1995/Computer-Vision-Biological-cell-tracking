import cv2 as cv

from boxes_drawer import BoxesDrawer
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
        return preprocessed_image

        # Segment image
        segmented_image = Watershed(preprocessed_image).perform()

        # Find segments
        segments = SegmentFinder(segmented_image).find()

        # Draw bounding box
        return BoxesDrawer(segments, image).draw()
