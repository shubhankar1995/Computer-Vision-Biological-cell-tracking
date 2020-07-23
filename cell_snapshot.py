from scipy.spatial.distance import euclidean


class CellSnapshot:
    def __init__(self, top_left, bottom_right, centroid):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.centroid = centroid
        self.prev_snapshot = None   # Prev snapshot (might be parent)
        self.cell = None    # Reference to the cell
        self.is_mitosis = False
        self.next_snapshots = list()  # Next snapshots (if > 1, they are children)
        self.speed = None

    def set_prev_snapshot(self, prev_snapshot):
        self.prev_snapshot = prev_snapshot

    def associate(self, cell):
        self.cell = cell

    def confirm_mitosis(self):
        self.is_mitosis = True

    def add_next_snapshot(self, snapshot):  # Also detect mitosis
        self.next_snapshots.append(snapshot)
        # Detect mitosis and mark
        next_snapshots_count = len(self.next_snapshots)
        if next_snapshots_count == 2:
            for snapshot in self.next_snapshots:
                snapshot.confirm_mitosis()
        elif next_snapshots_count > 2:
            snapshot.confirm_mitosis()

    def update_cell_mileage(self):
        if self.get_speed() is None:
            return

        self.cell.update_mileage(self.get_speed())

    def get_speed_display(self):
        if self.get_speed() is None:
            return 'N/A'

        return f'{self.get_speed():.2f}'

    def get_speed(self):
        if self.speed is not None:
            return self.speed

        if self.prev_snapshot is None:
            return

        self.speed = (
            euclidean(self.centroid, self.prev_snapshot.centroid)
        )
        return self.speed

    def get_total_distance(self):
        if self.cell is None:
            return 'N/A'

        return f'{self.cell.mileage:.2f}'

    def calc_net_distance(self):
        if self.cell is None:
            return 'N/A'

        return f'{euclidean(self.centroid, self.cell.origin):.2f}'
