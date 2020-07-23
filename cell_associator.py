import sys
import numpy as np
import cell_db

from cell import Cell
from directory_reader import DirectoryReader
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment


class CellAssociator:
    def __init__(self, curr_snapshots, prev_snapshots):
        self.curr_snapshots = curr_snapshots
        self.prev_snapshots = prev_snapshots
        self.distance_matrix = None

    def associate(self):
        subject_ids, object_ids = self.perform_linear_assignment()
        # Associate based on linear sum assignment (Primary)
        pri_associated_ids = self.assign(subject_ids, object_ids)

        # Mitosis or left-outs (Secondary)
        prim_unassociated_ids = sorted(list(     # Unassociated cells
            set(range(len(self.curr_snapshots))) - pri_associated_ids
        ))
        unas_curr_snapshots = self.curr_snapshots[prim_unassociated_ids]
        sec_dist_matrix = self.distance_matrix[prim_unassociated_ids, :]
        sec_object_ids = np.argmin(sec_dist_matrix, axis=1)  # nearest cell
        sec_associated_ids = self.assign(       # Assign based on argmin
            prim_unassociated_ids, sec_object_ids
        )

        # Recap all
        unassociated_ids = sorted(list(
            set(prim_unassociated_ids) - sec_associated_ids)
        )
        # Create new cell instances
        for unassociated_id in unassociated_ids:
            snapshot = self.curr_snapshots[unassociated_id]
            new_id = len(cell_db.cells)
            new_cell = Cell(new_id, snapshot.centroid)
            cell_db.cells.append(new_cell)
            snapshot.associate(new_cell)

        print(len(cell_db.cells))

        return self.curr_snapshots

    def perform_linear_assignment(self):
        # Build list of centroids
        curr_centroids = np.array([c.centroid for c in self.curr_snapshots])
        prev_centroids = np.array([c.centroid for c in self.prev_snapshots])

        # Calc distance matrix
        self.distance_matrix = cdist(curr_centroids, prev_centroids)

        # Assign
        return linear_sum_assignment(self.distance_matrix)

    def assign(self, subject_ids, object_ids):
        associated_ids = set()
        for i, subject_id in enumerate(subject_ids):
            object_id = object_ids[i]
            if self.distance_matrix[subject_id, object_id] > 15:
                continue  # Threshold

            subject_snapshot = self.curr_snapshots[subject_id]
            object_snapshot = self.prev_snapshots[object_id]
            subject_snapshot.set_prev_snapshot(object_snapshot)
            object_snapshot.add_next_snapshot(subject_snapshot)

            # Associate cells
            if len(object_snapshot.next_snapshots) == 1:  # Old cell
                subject_snapshot.associate(object_snapshot.cell)
            else:   # Mitosis
                new_id = len(cell_db.cells)
                new_cell = object_snapshot.cell.copy(new_id)
                cell_db.cells.append(new_cell)
                subject_snapshot.associate(new_cell)

            associated_ids.add(subject_id)

        return associated_ids


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
