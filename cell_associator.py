import sys
import numpy as np
import math
import global_vars

from cell import Cell
from directory_reader import DirectoryReader
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment


class CellAssociator:

    def __init__(self, curr_snapshots, prev_snapshots, threshold):
        self.curr_snapshots = curr_snapshots
        self.prev_snapshots = prev_snapshots
        self.distance_matrix = None
        self.threshold = threshold

    def associate(self):
        subject_ids, object_ids = self.perform_linear_sum_assignment()
        # Associate based on linear sum assignment (Primary)
        pri_associated_ids = self.assign(subject_ids, object_ids)

        # Mitosis or left-outs (Secondary)
        pri_unassociated_ids = sorted(list(     # Unassociated cells
            set(range(len(self.curr_snapshots))) - pri_associated_ids
        ))
        sec_dist_matrix = self.distance_matrix[pri_unassociated_ids, :]
        sec_object_ids = np.argmin(sec_dist_matrix, axis=1)  # nearest cell
        sec_associated_ids = self.assign(       # Assign based on argmin
            pri_unassociated_ids, sec_object_ids
        )

        # Initiate new cells for the unassigned
        unassociated_ids = sorted(list(
            set(pri_unassociated_ids) - sec_associated_ids
        ))
        self.initiate_new_cells(unassociated_ids)

        # Delete childless cells in prev
        for snapshot in self.prev_snapshots:
            if len(snapshot.next_snapshots) == 0:
                global_vars.cells[snapshot.cell.id] = None

    def perform_linear_sum_assignment(self):
        # Build list of centroids
        curr_centroids = np.array([c.centroid for c in self.curr_snapshots])
        prev_centroids = np.array([c.centroid for c in self.prev_snapshots])

        # Calc distance matrix
        self.distance_matrix = (
            cdist(curr_centroids, prev_centroids) /
            global_vars.image_diag
        )

        # Assign
        return linear_sum_assignment(self.distance_matrix)

    def assign(self, curr_ids, prev_ids):
        associated_ids = set()
        for i, curr_id in enumerate(curr_ids):
            prev_id = prev_ids[i]
            if self.distance_matrix[curr_id, prev_id] > self.threshold:
                continue  # Threshold

            curr_snapshot = self.curr_snapshots[curr_id]
            prev_snapshot = self.prev_snapshots[prev_id]
            curr_snapshot.set_prev_snapshot(prev_snapshot)
            prev_snapshot.add_next_snapshot(curr_snapshot)

            # Associate cells
            if len(prev_snapshot.next_snapshots) == 1:  # Old cell
                curr_snapshot.associate(prev_snapshot.cell)
            else:   # Mitosis
                new_id = len(global_vars.cells)
                new_cell = prev_snapshot.cell.copy(new_id)
                global_vars.cells.append(new_cell)
                curr_snapshot.associate(new_cell)

            # Update cell mileage (total dist)
            curr_snapshot.update_cell_mileage()

            associated_ids.add(curr_id)

        return associated_ids

    def initiate_new_cells(self, unassociated_ids):
        # Create new cell instances
        for unassociated_id in unassociated_ids:
            snapshot = self.curr_snapshots[unassociated_id]
            # Create new cell
            new_id = len(global_vars.cells)
            new_cell = Cell(new_id, snapshot.centroid)
            global_vars.cells.append(new_cell)
            # Associate
            snapshot.associate(new_cell)


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
