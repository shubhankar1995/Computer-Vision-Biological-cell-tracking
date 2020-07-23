import sys
import numpy as np

from directory_reader import DirectoryReader
from processor import Processor
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment


class CellAssociator:
    def __init__(prev_centroids, next_centroids):
        self.prev_centroids = prev_centroids
        self.next_centroids = next_centroids

    def associate(self):
        pass


if __name__ == '__main__':
    # cost = np.array([
    #     [8, 3, 5, 1, 0],
    #     [3, 9, 0, 5, 8],
    #     [4, 3, 8, 0, 3]
    # ])
    # print(cost)
    # row_idxs, col_idxs = linear_sum_assignment(cost)
    # print(row_idxs, len(row_idxs))
    # print(col_idxs, len(col_idxs))
    # print(cost[row_idxs, col_idxs].sum())
    # sys.exit()

    sequence_files = DirectoryReader(sys.argv[1]).get_sequence_files()
    mode = int(sys.argv[2])

    # Get segments & centroids
    _, prev_segments = Processor(sequence_files[0], mode).process()
    _, next_segments = Processor(sequence_files[1], mode).process()
    prev_centroids = np.array([x[2] for x in prev_segments])
    next_centroids = np.array([x[2] for x in next_segments])

    # Calc distance matrix
    distance_matrix = cdist(next_centroids, prev_centroids)
    print(next_centroids, len(next_centroids))
    print(prev_centroids, len(prev_centroids))
    print(distance_matrix, distance_matrix.shape)

    # Assignment
    row_idxs, col_idxs = linear_sum_assignment(distance_matrix)
    print(row_idxs, len(row_idxs))
    print(col_idxs, len(col_idxs))
