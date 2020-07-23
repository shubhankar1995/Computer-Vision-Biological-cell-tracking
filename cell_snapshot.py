class CellSnapshot:
    def __init__(self, top_left, bottom_right, centroid):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.centroid = centroid
        self.prev_snapshot = None   # Prev snapshot (might be parent)
        self.cell = None    # Reference to the cell
        self.is_mitosis = False

    def set_prev_snapshot(self, prev_snapshot):
        self.prev_snapshot = prev_snapshot

    def associate(self, cell):
        self.cell = cell

    def confirm_mitosis(self):
        self.is_mitosis = True
