import cv2 as cv
from collections import defaultdict
import sys
import math
from directory_reader import DirectoryReader
from watershed import Watershed
from segment_finder import SegmentFinder
from scipy.spatial import distance
import numpy as np
from scipy.optimize import linear_sum_assignment
import matplotlib.pyplot as plt

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

        # gray= cv.cvtColor(image,cv.COLOR_BGR2GRAY)

        detector = cv.xfeatures2d.SIFT_create(
            nfeatures=params["n_features"],
            nOctaveLayers=params["n_octave_layers"],
            contrastThreshold=params["contrast_threshold"],
            edgeThreshold=params["edge_threshold"],
            sigma=params["sigma"])

        kp1, des1 = detector.detectAndCompute(image, None)
        img1 = cv.drawKeypoints(image, kp1, image)
        cv.imwrite('sift_results/1-c.png', img1)
        return kp1

        # TODO: compare and keep those SIFT keypoints that are closest to the centroids found from SegmentFinder. Do this for all frames and compare keypoints in consequent frames using knnMatch in BFMatcher.

    def findClosestCentroid(self, kpt, centroids: list):
        cent_dict = dict()
        kpx, kpy = kpt
        for i, centroid in enumerate(centroids):
            dist = math.sqrt((kpx - centroid[0])**2 + (kpy - centroid[1])**2)
            cent_dict[i] = dist

        closest = min(cent_dict, key= cent_dict.get)
        return closest

    def isKp1CloserToCentroid(self, kpt1, kpt2, centroid):
        dist1 = math.sqrt((kpt1[0] - centroid[0])**2 + (kpt1[1] - centroid[1])**2)
        dist2 = math.sqrt((kpt2[0] - centroid[0])**2 + (kpt2[1] - centroid[1])**2)

        return True if dist1 < dist2 else False

    def filterKpByCentroids(self, keypoints, segments):

        centroids = [x[2] for x in segments]
        cent_kp_dict = dict.fromkeys(centroids, None)

        for i, kp in enumerate(keypoints):
            closest_centroid = self.findClosestCentroid(kp.pt, centroids)
            cent_val = centroids[closest_centroid]
            existing_kp = cent_kp_dict.get(cent_val)

            if existing_kp is None:
                cent_kp_dict[cent_val] = kp
            else:
                if self.isKp1CloserToCentroid(kp.pt, existing_kp.pt, cent_val):
                    cent_kp_dict[cent_val] = kp

        return cent_kp_dict

    def findDistance(self, prevCentroids, nextCentroids):
        distance_list = list()
        for prevCentroid in prevCentroids:
            # z = list().append(prevCentroid)
            # dist = distance.cdist(z, nextCentroids, "euclidean")
            dist = [distance.euclidean(prevCentroid, nextCentroid) for nextCentroid in nextCentroids]
            distance_list.append(dist)

        return np.array(distance_list)

    def getCentroidsFromSegments(self, segments):
        return [x[2] for x in segments]

    def addPositionToPath(self, indices, centroids, trajectoryDict: defaultdict):
        for k, v in enumerate(indices):
            trajectoryDict[k].append(centroids[v])

        return  trajectoryDict


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
    prev = None
    trajectoryDict = defaultdict(list)
    # Run
    print(f'There are {len(sequence_files)} images.')
    for i, file in enumerate(sequence_files):
        if i < 10:
            print(f'Processing file {i}...')
            # print(file)
            image = cv.imread(file, cv.IMREAD_GRAYSCALE)
            # cv.imshow('image', image)
            # cv.waitKey(0)
            # image= cv.cvtColor(image,cv.COLOR_BGR2GRAY)
            # image = Watershed(image).perform()
            # cellTracking.trackCell(image)
            # backtorgb = cv.cvtColor(image,cv.COLOR_GRAY2RGB)
            # gray_three = cv.merge([image,image,image])
            # cur_kp = cellTracking.siftFeatures(image)
            segmented_image = Watershed(image).perform()
            segments = SegmentFinder(segmented_image).find()
            centroids = cellTracking.getCentroidsFromSegments(segments)

            # cellTracking.filterKpByCentroids(cur_kp, segments)
            if prev is not None:
                graph = cellTracking.findDistance(prev, centroids)
                row_ind, col_ind = linear_sum_assignment(graph)
                trajectoryDict = cellTracking.addPositionToPath(col_ind, centroids, trajectoryDict)
            else:
                for k,v in enumerate(centroids):
                    trajectoryDict[k].append(v)
            prev = centroids
            print(f'File {i} done!')
    print(trajectoryDict)
    positions = trajectoryDict.get(0)
    x, y = list(), list()
    for pos in positions:
        y.append(pos[0])
        x.append(pos[1])

    # x.append(700)
    # y.append(11000)
    # plt.plot(testList2, linestyle='-', marker='o')
    # plt.scatter(testList2, linestyle='-', marker='o')
    w, h = image.shape()
    plt.plot(x, y)
    plt.xlim([0, w])
    plt.ylim([h, 0])
    plt.show()

