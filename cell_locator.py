import numpy as np

from cell_snapshot import CellSnapshot


class CellLocator:
    def __init__(self, labels):
        self.labels = labels

    def find(self):
        label_count = self.labels.max() + 1
        return [self.find_box(label) for label in range(1, label_count)]

    def find_box(self, label):
        indices = np.nonzero(self.labels == label)
        top, bottom = indices[0].min(), indices[0].max()
        left, right = indices[1].min(), indices[1].max()
        centroid = (
            (top + bottom) // 2,
            (left + right) // 2
        )

        return CellSnapshot((top, left), (bottom, right), centroid)
