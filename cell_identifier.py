class CellIdentifier:
    def __init__(self, segments, y, x):
        self.segments = segments
        self.y = y
        self.x = x

    def locate(self):
        for cell_id, segment in enumerate(self.segments):
            (top, left), (bottom, right), _ = segment
            if (
                top <= self.y and self.y <= bottom
                and left <= self.x and self.x <= right
            ):
                return cell_id

        return None
