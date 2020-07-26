import numpy as np


class TrackDrawer:
    def __init__(self, subplot, snapshots, image_size):
        self.subplot = subplot
        self.snapshots = snapshots
        self.image_size = image_size

    def draw(self):
        for c in self.snapshots:
            if c.prev_snapshot is not None and c.cell is not None:
                p = c.prev_snapshot
                self.subplot.plot(
                    [
                        self.cleanse(p.centroid[0], 0),
                        self.cleanse(c.centroid[0], 0)
                    ],
                    [
                        self.cleanse(p.centroid[1], 1),
                        self.cleanse(c.centroid[1], 1)
                    ],
                    linewidth=1, color=c.cell.color
                )

    def cleanse(self, coor, axis):  # axis, 0 = x, 1 = y
        return min(self.image_size[axis] - 1, max(0, np.intp(coor)))
