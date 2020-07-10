import numpy as np

class SegmentFinder:
    def __init__(self, labels):
        self.labels = labels

    def find(self):
        label_count = self.labels.max() + 1
        return [self.find_box(segment) for segment in range(1, label_count)]
    
    def find_box(self, label):
        indices = np.argwhere(self.labels == label)
        top_left, bottom_right = indices[0], indices[-1]
        centroid = (
            (bottom_right[0] + top_left[0]) // 2,
            (bottom_right[1] + top_left[1]) // 2
        )

        return top_left, bottom_right, centroid
    
