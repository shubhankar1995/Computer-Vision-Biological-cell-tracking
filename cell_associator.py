import sys
import numpy as np

from directory_reader import DirectoryReader
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment


class CellAssociator:
    def __init__(self, curr_snapshots, prev_snapshots):
        self.curr_snapshots = curr_snapshots
        self.prev_snapshots = prev_snapshots

    def associate(self):
        subject_ids, assigned_ids = self.assign()
        for i, subject_id in enumerate(subject_ids):
            assigned_snapshot = self.prev_snapshots[assigned_ids[i]]
            self.curr_snapshots[subject_id].associate(assigned_snapshot.cell)

    def assign(self):
        # Build list of centroids
        curr_centroids = np.array([c.centroid for c in self.curr_snapshots])
        prev_centroids = np.array([c.centroid for c in self.prev_snapshots])

        # Calc distance matrix
        distance_matrix = cdist(curr_centroids, prev_centroids)

        # Assign
        return linear_sum_assignment(distance_matrix)


if __name__ == '__main__':
    pass
    # sequence_files = DirectoryReader(sys.argv[1]).get_sequence_files()
    # mode = int(sys.argv[2])

    # Get segments & centroids
    # _, prev_segments = Processor(sequence_files[0], mode).process()
    # _, next_segments = Processor(sequence_files[1], mode).process()
    # prev_centroids = np.array([x[2] for x in prev_segments])
    # next_centroids = np.array([x[2] for x in next_segments])

    # Calc distance matrix
    # distance_matrix = cdist(next_centroids, prev_centroids)
    # print(next_centroids, len(next_centroids))
    # print(prev_centroids, len(prev_centroids))
    # print(distance_matrix, distance_matrix.shape)

    # # Assignment
    # row_idxs, col_idxs = linear_sum_assignment(distance_matrix)
    # print(row_idxs, len(row_idxs))
    # print(col_idxs, len(col_idxs))
