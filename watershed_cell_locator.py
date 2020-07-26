import numpy as np

from cell_snapshot import CellSnapshot


class WatershedCellLocator:
    def __init__(self, labels):
        self.labels = labels

    def locate(self):
        label_count = self.labels.max() + 1
        return np.array([
            self.locate_box(label) for label in range(1, label_count)
        ])

    def locate_box(self, label):
        indices = np.nonzero(self.labels == label)
        top, bottom = indices[0].min(), indices[0].max()
        left, right = indices[1].min(), indices[1].max()
        centroid = (
            (left + right) // 2,
            (top + bottom) // 2
        )
        size = right - left, top - bottom
        angle = 0   # Not rotated

        return CellSnapshot(centroid, size, angle)
