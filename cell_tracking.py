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

    def initialCellDict(self):
        segments = self.trackCell()
        cell_count = len(segments)
        for i in range(cell_count):
            self.master_cell_dict[i].append(segments[i][2])


    def siftFeatures(self, image):
        params = {}
        params["n_features"] = 0
        params["n_octave_layers"] = 3
        params["contrast_threshold"] = 0.1
        params["edge_threshold"] = 60
        params["sigma"] = 1.6

        gray= cv.cvtColor(image,cv.COLOR_BGR2GRAY)

        detector = cv.xfeatures2d.SIFT_create(
            nfeatures=params["n_features"],
            nOctaveLayers=params["n_octave_layers"],
            contrastThreshold=params["contrast_threshold"],
            edgeThreshold=params["edge_threshold"],
            sigma=params["sigma"])

        kp1, des1 = detector.detectAndCompute(image, None)
        img1 = cv.drawKeypoints(gray, kp1, image)
        cv.imwrite('sift_results/1-c.png', img1)

        # TODO: compare and keep those SIFT keypoints that are closest to the centroids found from SegmentFinder. Do this for all frames and compare keypoints in consequent frames using knnMatch in BFMatcher.
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
            # print(file)
            image = cv.imread(file)
            # image= cv.cvtColor(image,cv.COLOR_BGR2GRAY)
            # image = Watershed(image).perform()
            # cellTracking.trackCell(image)
            # backtorgb = cv.cvtColor(image,cv.COLOR_GRAY2RGB)
            # gray_three = cv.merge([image,image,image])
            cellTracking.siftFeatures(image)
            print(f'File {i} done!')
    