class Cell:
    def __init__(self, idx, origin, mileage=0):
        self.id = idx
        self.origin = origin
        self.mileage = mileage

    def copy(self):
        return Cell(self.id, self.origin, self.mileage)
