class CellIdentifier:
    def __init__(self, snapshots, y, x):
        self.snapshots = snapshots
        self.y = y
        self.x = x

    def identify(self):
        for cell_id, snapshot in enumerate(self.snapshots):
            (top, left) = snapshot.top_left
            (bottom, right) = snapshot.bottom_right
            if (
                top <= self.y and self.y <= bottom
                and left <= self.x and self.x <= right
            ):
                return cell_id

        return None
