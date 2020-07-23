class CellSnapshot:
    def __init__(self, top_left, bottom_right, centroid):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.centroid = centroid
        self.prev_snapshot = None   # Prev snapshot (might be parent)
        self.cell = None    # Reference to the cell
        self.is_mitosis = False
        self.next_snapshots = list()  # Next snapshots (if > 1, they are children)

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
